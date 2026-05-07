def choose_live_response(transcript: str, active_agent: str = "sinclair") -> str:
    text = transcript.strip()
    lowered = text.lower()

    if not text:
        return "I did not catch that clearly. Say that one more time for me."

    if any(phrase in lowered for phrase in ["can you hear me", "hello", "are you there"]):
        return "Yes. I can hear you. The live phone loop is working."

    if any(phrase in lowered for phrase in ["what can you do", "status", "where are we"]):
        return (
            "We have the phone line, media stream, and Sinclair voice online. "
            "The next layer is routing your request into the work system."
        )

    if active_agent == "khadijah":
        return (
            "I have the request. I do not have enough prepared context to answer that live, "
            "so I will turn it into follow-up work and come back with a proper brief."
        )

    return (
        "I heard you. I do not have that answer ready in the live context yet, "
        "so I will get back to you on that."
    )
