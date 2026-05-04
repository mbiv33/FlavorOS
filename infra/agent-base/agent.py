"""
FlavorOS Agent Runtime

A lightweight agent that:
1. Reads agent.yaml for identity, role, bus topics, and skill list
2. Loads SKILL.md files as system prompts
3. Subscribes to NATS for work orders
4. Calls the OpenRouter proxy for LLM completions
5. Publishes reports back to NATS
"""

import os, json, asyncio, logging, signal
from pathlib import Path
from glob import glob

import httpx, yaml, nats

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("agent")

NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")
OPENROUTER_URL = os.getenv("OPENROUTER_BASE_URL", "http://openrouter-proxy:8080/v1")
AGENT_CONFIG = os.getenv("AGENT_CONFIG", "/etc/flavoros/agent.yaml")
SKILLS_DIR = os.getenv("SKILLS_DIR", "/skills")
VAULT_PATH = os.getenv("VAULT_PATH", "/vault")
AGENT_NAME = os.getenv("AGENT_NAME", "unknown")


def load_config() -> dict:
    with open(AGENT_CONFIG) as f:
        return yaml.safe_load(f)


def load_skills(cfg: dict) -> dict[str, str]:
    """Load all SKILL.md files from mounted skills directories."""
    skills = {}
    for skill_dir in glob(f"{SKILLS_DIR}/*/"):
        skill_file = Path(skill_dir) / "SKILL.md"
        if skill_file.exists():
            skills[Path(skill_dir).name] = skill_file.read_text()
    return skills


def load_context_file(path: str) -> str:
    """Load a context file if it exists."""
    expanded = os.path.expandvars(path)
    if Path(expanded).exists():
        return Path(expanded).read_text()
    return ""


def build_system_prompt(cfg: dict, skills: dict[str, str], skill_name: str | None = None) -> str:
    """Build the system prompt from agent config and relevant skill."""
    parts = []

    parts.append(f"You are {cfg['name']}, role: {cfg['role']}.")

    soul_path = cfg.get("soul", "")
    if soul_path:
        soul = load_context_file(soul_path)
        if soul:
            parts.append(soul)

    context_path = cfg.get("context", "")
    if context_path:
        ctx = load_context_file(context_path)
        if ctx:
            parts.append(ctx)

    if skill_name and skill_name in skills:
        parts.append(skills[skill_name])
    elif skills:
        for name, content in skills.items():
            parts.append(content)

    vault_rules = cfg.get("vault", {})
    if vault_rules:
        parts.append(f"\nVault access — read: {vault_rules.get('read', [])}, write: {vault_rules.get('write', [])}")

    hitl = cfg.get("hitl", {})
    if hitl:
        escalate = hitl.get("always_escalates", hitl.get("always_drafts_for_approval", []))
        if escalate:
            parts.append(f"\nHuman-in-the-loop required for: {escalate}")

    return "\n\n---\n\n".join(parts)


def resolve_profile(cfg: dict, skill_name: str | None = None) -> str | None:
    """Resolve which model profile to use based on routing rules."""
    models = cfg.get("models", {})
    if "profiles" not in models:
        return None

    routing = models.get("routing_rules", [])
    if skill_name and routing:
        for rule in routing:
            if isinstance(rule, str) and skill_name in rule:
                return rule.split("→")[-1].strip()
            elif isinstance(rule, dict):
                if rule.get("skill") == skill_name:
                    return rule.get("profile", "thinking")
    return "thinking"


async def call_llm(agent_name: str, profile: str | None, messages: list[dict]) -> str:
    """Call the OpenRouter proxy for a completion."""
    headers = {
        "Content-Type": "application/json",
        "X-Agent-Name": agent_name,
    }
    if profile:
        headers["X-Agent-Profile"] = profile

    body = {
        "messages": messages,
        "max_tokens": 4096,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{OPENROUTER_URL}/chat/completions", json=body, headers=headers)

    if resp.status_code != 200:
        log.error("LLM call failed: %d %s", resp.status_code, resp.text[:500])
        return f"[error] LLM returned {resp.status_code}"

    data = resp.json()
    return data["choices"][0]["message"]["content"]


async def read_vault_file(path: str) -> str:
    """Read a file from the vault."""
    full = Path(VAULT_PATH) / path
    if full.exists():
        return full.read_text()
    return ""


async def handle_work_order(msg, cfg: dict, skills: dict[str, str], nc):
    """Process a single work order from NATS."""
    try:
        order = json.loads(msg.data.decode())
    except json.JSONDecodeError:
        log.error("invalid work order payload")
        return

    skill_name = order.get("skill", "")
    order_id = order.get("id", "unknown")
    args = order.get("args", {})

    log.info("received work_order: id=%s skill=%s args=%s", order_id, skill_name, args)

    system_prompt = build_system_prompt(cfg, skills, skill_name)
    profile = resolve_profile(cfg, skill_name)

    user_message = f"Execute skill: {skill_name}\n"
    if args:
        user_message += f"Arguments: {json.dumps(args)}\n"
    user_message += f"Current time: {order.get('fired_at', 'unknown')}\n"
    user_message += f"Respond with your report."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    log.info("calling LLM with profile=%s", profile)
    response = await call_llm(cfg["name"], profile, messages)

    report = {
        "agent": cfg["name"],
        "skill": skill_name,
        "order_id": order_id,
        "content": response,
    }

    report_subject = f"report.{cfg['name']}"
    await nc.publish(report_subject, json.dumps(report).encode())
    log.info("published report to %s (%d chars)", report_subject, len(response))


def read_secret(path: str) -> str:
    try:
        return Path(path).read_text().strip()
    except FileNotFoundError:
        return ""


async def telegram_poll(cfg: dict, skills: dict[str, str], nc):
    """Long-poll Telegram for messages and respond as the agent."""
    hi = cfg.get("human_interface", {})
    if hi.get("channel") != "telegram":
        return

    bot_token = read_secret(hi.get("bot_token_secret", ""))
    user_id = read_secret(hi.get("user_id_secret", ""))

    if not bot_token or not user_id or bot_token == "placeholder":
        log.warning("telegram credentials missing or placeholder; skipping bot")
        return

    log.info("starting telegram bot for user %s", user_id)
    api = f"https://api.telegram.org/bot{bot_token}"
    offset = 0

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            await client.post(f"{api}/sendMessage", json={
                "chat_id": int(user_id),
                "text": f"{cfg['name'].title()} online. Ready when you are.",
            })
        except Exception as e:
            log.error("telegram greeting failed: %s", e)

        while True:
            try:
                resp = await client.get(f"{api}/getUpdates", params={
                    "offset": offset,
                    "timeout": 30,
                })
                data = resp.json()
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "")
                    from_id = str(msg.get("from", {}).get("id", ""))

                    if from_id != user_id:
                        log.warning("ignoring message from unauthorized user %s", from_id)
                        continue
                    if not text:
                        continue

                    log.info("telegram received: %s", text[:80])

                    system_prompt = build_system_prompt(cfg, skills)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text},
                    ]

                    response = await call_llm(cfg["name"], None, messages)

                    for chunk in [response[i:i+4000] for i in range(0, len(response), 4000)]:
                        await client.post(f"{api}/sendMessage", json={
                            "chat_id": chat_id,
                            "text": chunk,
                        })
            except Exception as e:
                log.error("telegram poll error: %s", e)
                await asyncio.sleep(5)


async def run():
    cfg = load_config()
    agent_name = cfg["name"]
    log.name = agent_name
    log.info("starting agent: %s (%s)", agent_name, cfg["role"])

    skills = load_skills(cfg)
    log.info("loaded %d skills: %s", len(skills), list(skills.keys()))

    nc = await nats.connect(NATS_URL)
    log.info("connected to NATS")

    bus = cfg.get("bus", {})
    subscriptions = bus.get("subscribes", [])

    for subject in subscriptions:
        async def on_msg(msg, _cfg=cfg, _skills=skills, _nc=nc):
            await handle_work_order(msg, _cfg, _skills, _nc)

        await nc.subscribe(subject, cb=on_msg)
        log.info("subscribed to %s", subject)

    if not subscriptions:
        log.warning("no bus subscriptions configured — agent will idle")

    telegram_task = None
    if cfg.get("human_interface", {}).get("channel") == "telegram":
        telegram_task = asyncio.create_task(telegram_poll(cfg, skills, nc))

    stop = asyncio.Event()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)

    log.info("agent %s ready — waiting for work orders", agent_name)
    await stop.wait()

    if telegram_task:
        telegram_task.cancel()
    await nc.drain()
    log.info("agent %s shutting down", agent_name)


if __name__ == "__main__":
    asyncio.run(run())
