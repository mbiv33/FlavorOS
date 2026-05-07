import audioop
import io
import logging
import os
import wave
from pathlib import Path

import httpx


log = logging.getLogger("voice-gateway")

OPENAI_TRANSCRIPTIONS_URL = "https://api.openai.com/v1/audio/transcriptions"


def read_secret(path: str) -> str:
    try:
        return Path(path).read_text().strip()
    except FileNotFoundError:
        return ""


def openai_stt_configured() -> bool:
    api_key = read_secret(os.getenv("OPENAI_API_KEY_FILE", ""))
    return bool(api_key and api_key != "placeholder")


def ulaw_to_wav_bytes(ulaw_audio: bytes) -> bytes:
    pcm = audioop.ulaw2lin(ulaw_audio, 2)
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(8000)
        wav.writeframes(pcm)
    return output.getvalue()


async def transcribe_ulaw(ulaw_audio: bytes) -> str:
    api_key = read_secret(os.getenv("OPENAI_API_KEY_FILE", ""))
    model = os.getenv("OPENAI_TRANSCRIBE_MODEL", "whisper-1")
    if not api_key:
        raise RuntimeError("OpenAI transcription key missing")

    wav_audio = ulaw_to_wav_bytes(ulaw_audio)
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {
        "file": ("twilio.wav", wav_audio, "audio/wav"),
    }
    data = {
        "model": model,
        "response_format": "json",
        "language": "en",
    }

    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post(
            OPENAI_TRANSCRIPTIONS_URL,
            headers=headers,
            data=data,
            files=files,
        )

    if response.status_code >= 400:
        raise RuntimeError(f"OpenAI transcription failed {response.status_code}: {response.text[:300]}")

    text = response.json().get("text", "").strip()
    log.info("stt transcript chars=%d", len(text))
    return text
