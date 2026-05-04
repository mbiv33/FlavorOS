FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir httpx uvicorn starlette pyyaml

COPY proxy.py /app/proxy.py

EXPOSE 8080

CMD ["python", "proxy.py"]
