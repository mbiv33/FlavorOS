Gemini 3.1 Flash Voice & Twilio Voice Streaming: Deep‑Dive Analysis

This report analyses Google’s Gemini 3.1 Flash voice capabilities and Twilio’s Programmable Voice Media Streams APIs.  It explains how to build a low‑latency voice pipeline that can connect a phone call to Gemini’s multimodal model, and summarises key features, API formats and integration challenges.  Citations come from official documentation and blogs.

1 Gemini 3.1 Flash voice

1.1 Gemini Live API overview

Gemini’s Live API turns the model into an interactive voice system.  Developers open a bidirectional WebSocket session and stream audio, text and images; the API returns partial or final spoken responses with extremely low latency .  The core features include:

* Low‑latency real‑time dialogue – the Live API streams responses before a turn has finished (sentence‑by‑sentence), enabling overlapping speech (barge‑in) and natural interruption .  This eliminates long wait times typical of text‑only LLM calls.
* Multilingual & tonal awareness – Gemini 3.1 Flash is fine‑tuned for human‑like conversation.  Google claims improved tone and tempo recognition compared with earlier models , and it supports multiple languages without explicit configuration .
* Tool use and audio transcription – the API can call tools (functions) mid‑conversation and return transcribed user speech, which is useful for pipeline integration .  It can also proactively change audio characteristics or adjust volume and pitch during a session (affective dialogue) .
* Audio watermarking – all generated audio is watermarked using SynthID so that downstream applications can detect AI‑generated speech .  This supports compliance and content authenticity.

1.2 Audio formats and WebSocket messages

The Live API accepts raw 16‑bit PCM audio sampled at 16 kHz as input, and returns audio at 24 kHz .  Developers connect via a URL of the form
wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key=API_KEY .  Google recommends using short‑lived ephemeral tokens rather than long‑lived API keys for security .

A live session starts by sending a JSON configuration message specifying the model (e.g., "gemini-2.5-flash" or "gemini-3.1-flash"), the expected output modalities (["AUDIO"]), a system instruction with role guidance and voice settings, and optional tool definitions .  Afterwards, the client continuously sends either text prompts or binary audio messages with the MIME type audio/pcm;rate=16000 .  The server responds with streamed deltas containing partial text and audio buffers; once complete, it ends the turn.

1.3 Gemini 3.1 Flash TTS features

Google’s TTS service builds on Gemini to generate high‑quality speech.  The updated Flash TTS model (2025) introduces audio tags for style control: developers can alter vocal style, pacing or accent using natural‑language tags in the input .  Gemini TTS supports 70+ languages and includes prebuilt voices like Kore, Zephyr or Puck .  Output is watermarked with SynthID for provenance .  Styles and voices can be exported from the web UI to code for consistent reuse .

2 Twilio Programmable Voice Media Streams

Twilio’s Media Streams allow developers to fork audio from a live call to a WebSocket and, with bidirectional streams, pipe audio back into the call.  The <Start><Stream> verb creates a unidirectional stream (receive only), while <Connect><Stream> creates a bidirectional stream .

2.1 Starting a stream

* Unidirectional stream: Place <Start><Stream> in your TwiML.  Twilio immediately begins streaming the call’s audio to the provided wss:// endpoint and continues executing subsequent TwiML instructions .  Use attributes:
    * url – WebSocket endpoint (must be wss:// and cannot include query parameters ).
    * name – optional unique identifier used to stop the stream later .
    * track – inbound_track, outbound_track or both_tracks; defaults to inbound_track .
    * statusCallback – absolute URL that Twilio notifies when a stream starts or stops, including parameters such as StreamSid, StreamEvent, and error messages .
    * custom <Parameter> tags to pass arbitrary metadata; Twilio sends these values in the start.customParameters of the first WebSocket message .
* Bidirectional stream: Use <Connect><Stream> to enable two‑way audio.  In this mode Twilio pauses executing further TwiML until the WebSocket closes .  Bidirectional streams only support the inbound_track for receiving audio .

2.2 WebSocket messages from Twilio

During a Media Stream, Twilio sends several structured JSON messages to your WebSocket server :