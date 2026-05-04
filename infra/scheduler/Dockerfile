FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir nats-py pyyaml croniter

COPY scheduler.py /app/scheduler.py

CMD ["python", "scheduler.py"]
