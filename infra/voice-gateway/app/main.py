import asyncio
import audioop
import base64
import json
import logging
import math
import os
from datetime import datetime, timezone
from urllib.parse import parse_qs

from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect

from .elevenlabs_tts import elevenlabs_configured, synthesize_ulaw
from .openai_stt import openai_stt_configured, transcribe_ulaw
from .policy import choose_live_response


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [voice-gateway] %(levelname)s %(message)s",
)
log = logging.getLogger("voice-gateway")

app = FastAPI(title="FlavorOS Voice Gateway")

SAMPLE_RATE = 8000
CHUNK_MS = 20
SAMPLES_PER_CHUNK = SAMPLE_RATE * CHUNK_MS // 1000
UTTERANCE_CHUNKS = int(os.getenv("VOICE_UTTERANCE_CHUNKS", "140"))
CAPTURE_MODE = os.getenv("VOICE_CAPTURE_MODE", "fixed").strip().lower()
MIN_UTTERANCE_CHUNKS = int(os.getenv("VOICE_MIN_UTTERANCE_CHUNKS", "6"))
MAX_UTTERANCE_CHUNKS = int(os.getenv("VOICE_MAX_UTTERANCE_CHUNKS", str(UTTERANCE_CHUNKS)))
SILENCE_CHUNKS = int(os.getenv("VOICE_SILENCE_CHUNKS", "8"))
SILENCE_RMS_THRESHOLD = int(os.getenv("VOICE_SILENCE_RMS_THRESHOLD", "350"))


def stream_url() -> str:
    return os.getenv("TWILIO_STREAM_URL", "wss://voice.flavoros.bairyos.com/twilio-stream")


async def safe_send_json(websocket: WebSocket, payload: dict) -> bool:
    try:
        await websocket.send_json(payload)
        return True
    except RuntimeError as exc:
        log.info("websocket send skipped: %s", exc)
        return False


def linear_to_mulaw(sample: int) -> int:
    """Convert signed 16-bit PCM to G.711 mu-law for Twilio media streams."""
    bias = 0x84
    clip = 32635

    sign = 0x80 if sample < 0 else 0
    if sample < 0:
        sample = -sample
    sample = min(sample, clip) + bias

    exponent = 7
    mask = 0x4000
    while exponent > 0 and not (sample & mask):
        exponent -= 1
        mask >>= 1

    mantissa = (sample >> (exponent + 3)) & 0x0F
    return (~(sign | (exponent << 4) | mantissa)) & 0xFF


def ulaw_rms(ulaw_audio: bytes) -> int:
    if not ulaw_audio:
        return 0
    pcm = audioop.ulaw2lin(ulaw_audio, 2)
    return audioop.rms(pcm, 2)


def test_tone_payloads(duration_seconds: float = 0.8, frequency_hz: float = 660.0) -> list[str]:
    total_samples = int(SAMPLE_RATE * duration_seconds)
    encoded = bytearray()

    for i in range(total_samples):
        envelope = min(1.0, i / 400, (total_samples - i) / 400)
        amplitude = int(9000 * max(0.0, envelope))
        sample = int(amplitude * math.sin(2 * math.pi * frequency_hz * i / SAMPLE_RATE))
        encoded.append(linear_to_mulaw(sample))

    payloads = []
    for start in range(0, len(encoded), SAMPLES_PER_CHUNK):
        chunk = bytes(encoded[start:start + SAMPLES_PER_CHUNK])
        payloads.append(base64.b64encode(chunk).decode("ascii"))
    return payloads


async def send_test_tone(websocket: WebSocket, stream_sid: str) -> None:
    for payload in test_tone_payloads():
        if not await safe_send_json(websocket, {
            "event": "media",
            "streamSid": stream_sid,
            "media": {"payload": payload},
        }):
            return
        await asyncio.sleep(CHUNK_MS / 1000)

    await safe_send_json(websocket, {
        "event": "mark",
        "streamSid": stream_sid,
        "mark": {"name": "flavoros-test-tone"},
    })
    log.info("sent test tone stream_sid=%s", stream_sid)


async def send_ulaw_audio(websocket: WebSocket, stream_sid: str, audio: bytes, mark_name: str) -> None:
    for start in range(0, len(audio), SAMPLES_PER_CHUNK):
        chunk = audio[start:start + SAMPLES_PER_CHUNK]
        if not await safe_send_json(websocket, {
            "event": "media",
            "streamSid": stream_sid,
            "media": {"payload": base64.b64encode(chunk).decode("ascii")},
        }):
            return
        await asyncio.sleep(CHUNK_MS / 1000)

    await safe_send_json(websocket, {
        "event": "mark",
        "streamSid": stream_sid,
        "mark": {"name": mark_name},
    })
    log.info("sent ulaw audio stream_sid=%s mark=%s bytes=%d", stream_sid, mark_name, len(audio))


async def send_clear(websocket: WebSocket, stream_sid: str) -> None:
    await safe_send_json(websocket, {
        "event": "clear",
        "streamSid": stream_sid,
    })
    log.info("sent clear stream_sid=%s", stream_sid)


async def send_text_response(websocket: WebSocket, stream_sid: str, text: str, mark_name: str) -> None:
    if elevenlabs_configured():
        audio = await synthesize_ulaw(text)
        await send_ulaw_audio(websocket, stream_sid, audio, mark_name)
        return

    log.warning("ElevenLabs missing; falling back to test tone")
    await send_test_tone(websocket, stream_sid)


async def send_opening_response(websocket: WebSocket, stream_sid: str) -> None:
    opening_mode = os.getenv("VOICE_OPENING_MODE", "disabled").strip().lower()
    if opening_mode in {"disabled", "off", "none", ""}:
        log.info("voice opening response disabled")
        return

    mode = os.getenv("VOICE_REPLY_MODE", "test_tone").strip().lower()
    active_agent = os.getenv("VOICE_ACTIVE_AGENT", "sinclair").strip().lower()

    if mode == "elevenlabs_static":
        if not elevenlabs_configured():
            log.warning("ElevenLabs mode requested but key/voice is missing; falling back to test tone")
            await send_test_tone(websocket, stream_sid)
            return

        text = (
            "Sinclair here. I can hear you. "
            "This line is a live audio-path test, not the full assistant yet."
        )
        if active_agent == "khadijah":
            text = (
                "Khadijah here. I can hear you. "
                "This is a live audio-path test before we turn on full briefing mode."
            )
        await send_text_response(websocket, stream_sid, text, f"{active_agent}-elevenlabs-opening")
        return

    if mode not in {"test_tone", "disabled", ""}:
        log.warning("unknown VOICE_REPLY_MODE=%s; using test_tone", mode)

    if mode == "disabled":
        log.info("voice opening response disabled")
        return

    await send_test_tone(websocket, stream_sid)


async def handle_utterance(websocket: WebSocket, stream_sid: str, ulaw_audio: bytes) -> None:
    active_agent = os.getenv("VOICE_ACTIVE_AGENT", "sinclair").strip().lower()
    stt_mode = os.getenv("VOICE_STT_MODE", "openai_batch").strip().lower()

    if stt_mode in {"disabled", "off", "none"}:
        log.info("stt disabled; skipping utterance")
        return

    if stt_mode != "openai_batch":
        log.warning("unknown VOICE_STT_MODE=%s; using openai_batch", stt_mode)

    if not openai_stt_configured():
        log.warning("OpenAI STT missing; speaking defer response without transcript")
        response = choose_live_response("", active_agent)
        await send_text_response(websocket, stream_sid, response, f"{active_agent}-no-stt")
        return

    try:
        transcript = await transcribe_ulaw(ulaw_audio)
    except Exception as exc:
        log.error("stt failed: %s", exc)
        response = "I had trouble catching that clearly. I will get back to you on that."
        await send_text_response(websocket, stream_sid, response, f"{active_agent}-stt-error")
        return

    log.info("caller transcript=%s", transcript[:200])
    response = choose_live_response(transcript, active_agent)
    await send_text_response(websocket, stream_sid, response, f"{active_agent}-policy-response")


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "voice-gateway",
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.api_route("/voice", methods=["GET", "POST"])
async def voice_webhook(request: Request) -> Response:
    raw_body = await request.body() if request.method == "POST" else b""
    form = parse_qs(raw_body.decode("utf-8", errors="ignore"))
    call_sid = form.get("CallSid", [""])[0]
    from_number = form.get("From", [""])[0]
    log.info("voice webhook received call_sid=%s from_present=%s", call_sid, bool(from_number))

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Connect>
    <Stream url="{stream_url()}" />
  </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")


@app.websocket("/twilio-stream")
async def twilio_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    log.info("twilio stream connected")
    stream_sid = ""
    inbound_audio = bytearray()
    media_chunks_seen = 0
    speech_started = False
    speech_chunks = 0
    trailing_silence_chunks = 0
    closed = False
    utterances_started = 0
    utterance_task: asyncio.Task | None = None
    playback_task: asyncio.Task | None = None

    try:
        while True:
            message = await websocket.receive_text()
            try:
                event = json.loads(message)
            except json.JSONDecodeError:
                log.warning("twilio stream non-json message len=%d", len(message))
                continue

            event_type = event.get("event", "unknown")
            if event_type == "media":
                media = event.get("media", {})
                chunk = media.get("chunk", "")
                payload = media.get("payload", "")
                chunk_audio = b""
                if payload:
                    try:
                        chunk_audio = base64.b64decode(payload)
                        inbound_audio.extend(chunk_audio)
                    except Exception:
                        log.warning("invalid media payload chunk=%s", chunk)

                media_chunks_seen += 1
                rms = ulaw_rms(chunk_audio)
                if rms >= SILENCE_RMS_THRESHOLD:
                    speech_started = True
                    speech_chunks += 1
                    trailing_silence_chunks = 0
                elif speech_started:
                    trailing_silence_chunks += 1

                if str(chunk).endswith("0"):
                    log.info(
                        "twilio media chunk=%s payload_len=%d rms=%d",
                        chunk,
                        len(payload),
                        rms,
                    )
                if CAPTURE_MODE == "silence":
                    should_process = (
                        stream_sid
                        and speech_started
                        and speech_chunks >= MIN_UTTERANCE_CHUNKS
                        and (
                            trailing_silence_chunks >= SILENCE_CHUNKS
                            or media_chunks_seen >= MAX_UTTERANCE_CHUNKS
                        )
                    )
                else:
                    should_process = (
                        stream_sid
                        and len(inbound_audio) >= UTTERANCE_CHUNKS * SAMPLES_PER_CHUNK
                    )

                should_process = (
                    should_process
                    and (utterance_task is None or utterance_task.done())
                    and (playback_task is None or playback_task.done())
                    and utterances_started < 1
                )
                if should_process:
                    audio = bytes(inbound_audio)
                    inbound_audio.clear()
                    utterances_started += 1
                    log.info(
                        "utterance captured chunks=%d speech_chunks=%d trailing_silence=%d bytes=%d",
                        media_chunks_seen,
                        speech_chunks,
                        trailing_silence_chunks,
                        len(audio),
                    )
                    utterance_task = asyncio.create_task(handle_utterance(websocket, stream_sid, audio))
                continue

            if event_type == "start":
                start = event.get("start", {})
                stream_sid = start.get("streamSid", "")
                log.info(
                    "twilio start stream_sid=%s call_sid=%s",
                    stream_sid,
                    start.get("callSid", ""),
                )
                if stream_sid:
                    playback_task = asyncio.create_task(send_opening_response(websocket, stream_sid))
                continue

            if event_type == "dtmf" and stream_sid:
                if playback_task and not playback_task.done():
                    playback_task.cancel()
                    await send_clear(websocket, stream_sid)
                continue

            log.info("twilio event=%s", event_type)
    except WebSocketDisconnect:
        closed = True
        log.info("twilio stream disconnected")
    except Exception as exc:
        closed = True
        log.exception("twilio stream error: %s", exc)
    finally:
        closed = True
        for task in (utterance_task, playback_task):
            if task and not task.done():
                task.cancel()
