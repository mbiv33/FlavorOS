
## VPS Inventory

- Generated at: 2026-05-06T17:01:22Z
- Hostname: REDACTED_HOSTNAME
- User: root

## OS

### uname

```text
Linux REDACTED_HOSTNAME 6.8.0-107-generic #107-Ubuntu SMP PREEMPT_DYNAMIC Fri Mar 13 19:51:50 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```

### os-release

```text
PRETTY_NAME="Ubuntu 24.04.4 LTS"
VERSION_ID="24.04"
VERSION="24.04.4 LTS (Noble Numbat)"
ID=ubuntu
```


## Network

### listening ports

```text
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                                                  
udp   UNCONN 0      0         127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=51857,fd=16))             
udp   UNCONN 0      0      127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=51857,fd=14))             
tcp   LISTEN 0      4096   127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=51857,fd=15))             
tcp   LISTEN 0      4096         0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=57880,fd=3),("systemd",pid=1,fd=107))
tcp   LISTEN 0      4096         0.0.0.0:32773      0.0.0.0:*    users:(("docker-proxy",pid=37653,fd=8))                 
tcp   LISTEN 0      4096         0.0.0.0:32769      0.0.0.0:*    users:(("docker-proxy",pid=7518,fd=8))                  
tcp   LISTEN 0      4096      127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=51857,fd=17))             
tcp   LISTEN 0      4096         0.0.0.0:58993      0.0.0.0:*    users:(("docker-proxy",pid=4147,fd=8))                  
tcp   LISTEN 0      4096            [::]:22            [::]:*    users:(("sshd",pid=57880,fd=4),("systemd",pid=1,fd=108))
tcp   LISTEN 0      4096            [::]:32773         [::]:*    users:(("docker-proxy",pid=37659,fd=8))                 
tcp   LISTEN 0      4096            [::]:32769         [::]:*    users:(("docker-proxy",pid=7523,fd=8))                  
tcp   LISTEN 0      4096               *:80               *:*    users:(("traefik",pid=1381,fd=4))                       
tcp   LISTEN 0      4096               *:443              *:*    users:(("traefik",pid=1381,fd=7))                       
tcp   LISTEN 0      4096            [::]:58993         [::]:*    users:(("docker-proxy",pid=4153,fd=8))                  
```

### public ip probe

```text
REDACTED_PUBLIC_IP```


## Git

### git version

```text
git version 2.43.0
```

No git repo detected in current directory.


## Docker

### docker version

```text
Docker version 29.4.0, build 9d7ad9f
```

### docker compose version

```text
Docker Compose version v5.1.2
```

### docker ps

```text
NAMES                              IMAGE                                        STATUS        PORTS
hermes-agent-isuk-hermes-agent-1   ghcr.io/hostinger/hvps-hermes-agent:latest   Up 46 hours   0.0.0.0:32769->4860/tcp, [::]:32769->4860/tcp
openclaw-pn8l-openclaw-1           ghcr.io/hostinger/hvps-openclaw:latest       Up 2 days     0.0.0.0:58993->58993/tcp, [::]:58993->58993/tcp
hermes-agent-kxed-hermes-agent-1   ghcr.io/hostinger/hvps-hermes-agent:latest   Up 44 hours   0.0.0.0:32773->4860/tcp, [::]:32773->4860/tcp
traefik-traefik-1                  traefik:latest                               Up 2 days     
```

### docker images

```text
REPOSITORY                            TAG       IMAGE ID       CREATED       SIZE
traefik                               latest    8cb20d16e01a   6 days ago    245MB
ghcr.io/hostinger/hvps-openclaw       latest    65648773caab   2 weeks ago   5.3GB
ghcr.io/hostinger/hvps-hermes-agent   latest    7fc18af3c7a1   3 weeks ago   8.41GB
```

### docker networks

```text
NETWORK ID     NAME                        DRIVER    SCOPE
554dd34848b0   bridge                      bridge    local
80cd834cccc9   hermes-agent-isuk_default   bridge    local
07b32e0c34d7   hermes-agent-kxed_default   bridge    local
989f932f0121   host                        host      local
800c3d88a8ab   none                        null      local
0da8d85e0548   openclaw-pn8l_default       bridge    local
```

### docker volumes

```text
DRIVER    VOLUME NAME
local     traefik-letsencrypt
local     traefik_traefik-letsencrypt
```


## Compose

No compose file detected in current directory.


## Reverse Proxy

### caddy status

```text
```

### nginx status

```text
```

### traefik containers

```text
traefik-traefik-1 traefik:latest
```


## FlavorOS Paths

### candidate app dirs

```text
```

### repo top files

```text
/root
```


## Environment Names Only

### process env names

```text
DBUS_SESSION_BUS_ADDRESS
HOME
LANG
LOGNAME
PATH
PWD
SHELL
SHLVL
SSH_CLIENT
SSH_CONNECTION
USER
XDG_RUNTIME_DIR
XDG_SESSION_CLASS
XDG_SESSION_ID
XDG_SESSION_TYPE
_
```


## Recent Logs

Skipped by default. Re-run with INCLUDE_LOGS=1 only after confirming logs do not contain raw secrets.


## Inventory Complete

Review this file before running deploy or secrets commands.
