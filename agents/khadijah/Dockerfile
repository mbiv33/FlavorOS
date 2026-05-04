FROM ghcr.io/nousresearch/hermes-agent:latest

WORKDIR /app

# Skills + soul are bind-mounted at runtime (see docker-compose.yml).
# Hermes reads /etc/flavoros/agent.yaml on boot.

ENV AGENT_CONFIG=/etc/flavoros/agent.yaml \
    SKILLS_DIR=/skills \
    LOG_LEVEL=info

CMD ["hermes", "run", "--config", "/etc/flavoros/agent.yaml"]
