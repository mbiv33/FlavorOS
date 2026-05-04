FROM alpine:3.20

RUN apk add --no-cache age sops jq bash py3-pip \
 && pip install --break-system-packages yq

COPY entrypoint.sh /usr/local/bin/load-secrets
RUN chmod +x /usr/local/bin/load-secrets

ENTRYPOINT ["/usr/local/bin/load-secrets"]
