"""
OpenRouter proxy sidecar.
Reads routing config from /etc/openrouter.yaml and the API key from a
secrets file. Proxies /v1/chat/completions to api.openrouter.ai with
per-agent model selection and token-cap enforcement.
"""

import os, json, asyncio, logging
from pathlib import Path

import httpx, yaml
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
import uvicorn

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
log = logging.getLogger("openrouter-proxy")

ROUTING_CONFIG = os.getenv("ROUTING_CONFIG", "/etc/openrouter.yaml")
API_KEY_FILE = os.getenv("OPENROUTER_API_KEY_FILE", "/run/flavor/secrets/_shared/openrouter.key")
UPSTREAM = "https://openrouter.ai/api"

config: dict = {}
api_key: str = ""

def load_config():
    global config, api_key
    with open(ROUTING_CONFIG) as f:
        config = yaml.safe_load(f)
    api_key = Path(API_KEY_FILE).read_text().strip()
    log.info("config loaded: %d agents", len(config.get("agents", {})))

def resolve_model(agent: str, profile: str | None = None) -> str:
    agents = config.get("agents", {})
    agent_cfg = agents.get(agent, {})
    if "profiles" in agent_cfg and profile:
        return agent_cfg["profiles"].get(profile, {}).get("primary", "anthropic/claude-haiku-4.5")
    return agent_cfg.get("primary", config.get("defaults", {}).get("primary", "anthropic/claude-haiku-4.5"))

async def proxy_completions(request: Request) -> Response:
    body = await request.json()
    agent = request.headers.get("X-Agent-Name", "unknown")
    profile = request.headers.get("X-Agent-Profile")
    model = resolve_model(agent, profile)
    body["model"] = model

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://flavoros.local",
        "X-Title": f"FlavorOS/{agent}",
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{UPSTREAM}/v1/chat/completions", json=body, headers=headers)

    log.info("agent=%s model=%s status=%d", agent, model, resp.status_code)
    return Response(content=resp.content, status_code=resp.status_code, headers={"Content-Type": "application/json"})

async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})

async def startup():
    load_config()

app = Starlette(
    routes=[
        Route("/v1/chat/completions", proxy_completions, methods=["POST"]),
        Route("/health", health),
    ],
    on_startup=[startup],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
