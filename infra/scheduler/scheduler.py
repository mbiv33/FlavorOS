"""
Cron scheduler: reads schedules.yaml and publishes work_order.<agent>
messages on NATS at the configured times.
"""

import os, json, asyncio, logging
from datetime import datetime, timezone

import yaml, nats
from croniter import croniter

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
log = logging.getLogger("scheduler")

NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")
SCHEDULES_FILE = os.getenv("SCHEDULES", "/etc/schedules.yaml")

async def run():
    with open(SCHEDULES_FILE) as f:
        cfg = yaml.safe_load(f)

    schedules = cfg.get("schedules", [])
    log.info("loaded %d schedules", len(schedules))

    nc = await nats.connect(NATS_URL)
    log.info("connected to NATS at %s", NATS_URL)

    iters = {}
    for s in schedules:
        iters[s["id"]] = croniter(s["cron"], datetime.now())

    while True:
        now = datetime.now()
        nearest_wait = 60.0

        for s in schedules:
            cit = iters[s["id"]]
            next_fire = cit.get_next(datetime)

            wait = (next_fire - now).total_seconds()
            if wait <= 0:
                subject = f"work_order.{s['agent']}"
                payload = json.dumps({
                    "id": s["id"],
                    "agent": s["agent"],
                    "skill": s.get("skill", ""),
                    "args": s.get("args", {}),
                    "fired_at": datetime.now(timezone.utc).isoformat(),
                }).encode()

                await nc.publish(subject, payload)
                log.info("fired %s -> %s", s["id"], subject)
                iters[s["id"]] = croniter(s["cron"], datetime.now())
            else:
                nearest_wait = min(nearest_wait, wait)

        await asyncio.sleep(min(nearest_wait, 30))

if __name__ == "__main__":
    asyncio.run(run())
