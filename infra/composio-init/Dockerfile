FROM python:3.12-slim
RUN pip install --no-cache-dir composio-core==0.* pyyaml httpx[http2] qrcode
COPY init.py /usr/local/bin/composio-init
RUN chmod +x /usr/local/bin/composio-init
ENTRYPOINT ["composio-init"]
