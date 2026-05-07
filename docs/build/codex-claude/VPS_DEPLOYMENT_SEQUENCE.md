# VPS Deployment Sequence

## Phase 1 — Server Foundation

```bash
ssh root@YOUR_SERVER_IP
apt update && apt upgrade -y
apt install -y git curl wget ufw fail2ban ca-certificates gnupg lsb-release unzip jq nano htop
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Harden SSH:

```bash
nano /etc/ssh/sshd_config
```

Set:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart:

```bash
systemctl restart ssh
```

Firewall:

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status verbose
```

Swap:

```bash
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab
```

## Phase 2 — Docker

```bash
apt install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
usermod -aG docker deploy
```

Log out and back in as deploy.

## Phase 3 — Reverse Proxy

Install Caddy:

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy
```

Caddyfile:

```caddy
voice.yourdomain.com {
    encode gzip
    reverse_proxy 127.0.0.1:8088
}
```

Reload:

```bash
sudo systemctl reload caddy
```

## Phase 4 — Repo

```bash
ssh deploy@YOUR_SERVER_IP
mkdir -p ~/apps
cd ~/apps
git clone YOUR_REPO_URL flavoros
cd flavoros
mkdir -p vault workspace cron infra/secrets logs backups scripts
cp .env.example .env
nano .env
chmod 600 .env
```

## Phase 5 — Base Services

```bash
docker compose config
docker compose build
docker compose up -d nats redis postgres openrouter-proxy secrets-loader scheduler vault-sync
docker compose ps
```

## Phase 6 — Agents

```bash
docker compose up -d khadijah sinclair maxine scooter kyle
docker compose ps
docker compose logs -f khadijah
```

## Phase 7 — Voice Gateway

```bash
docker compose build voice-gateway
docker compose up -d voice-gateway
docker compose logs -f voice-gateway
curl https://voice.yourdomain.com/health
```

## Phase 8 — Twilio

Set Twilio incoming call webhook:

```text
https://voice.yourdomain.com/voice
```

The app returns TwiML pointing to:

```text
wss://voice.yourdomain.com/twilio-stream
```
