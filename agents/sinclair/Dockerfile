FROM ghcr.io/openclaw/agent:latest

WORKDIR /app

ENV AGENT_CONFIG=/etc/flavoros/agent.yaml \
    SKILLS_DIR=/skills \
    LOG_LEVEL=info

CMD ["openclaw", "run", "--config", "/etc/flavoros/agent.yaml"]
