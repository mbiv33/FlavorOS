FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    httpx \
    nats-py \
    pyyaml \
    redis \
    asyncpg \
    pgvector

COPY agent.py /app/agent.py

ENV AGENT_CONFIG=/etc/flavoros/agent.yaml \
    SKILLS_DIR=/skills \
    LOG_LEVEL=info

CMD ["python", "agent.py"]
