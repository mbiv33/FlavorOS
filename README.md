# FlavorOS
## "Keeping it Professional. Keeping it Flavor."

AI skills that run your day — inbox, tasks, follow-ups, wellness, and the operating rhythm that holds it together.

Built for [Hermes Agent](https://hermes-agent.nousresearch.com/). Inspired by [clawchief](https://github.com/snarktank/clawchief).

---

## What This Is

FlavorOS is a multi-agent executive operating system built on a **Hub-and-Spoke model**. Khadijah — your Conductor and Chief of Staff — orchestrates a team of specialized agents, each with a distinct role and personality. The system handles the **Identify → Research → Draft** cycle so you only handle the **Decide → Act** cycle.

**Human-in-the-Loop (HITL):** No agent spends money, RSVPs to events, or commits your time without your explicit "Editorial Approval." You are the Sovereign Approver.

## The Staff

| Agent | Role | Skill |
|-------|------|-------|
| **Khadijah James** | Chief of Staff & Conductor | `chief-of-staff` |
| **Sinclair James** | Executive Assistant & Scheduling | `executive-assistant` |
| **Maxine Shaw** | Project Management & Growth | `daily-task-manager` |
| **Kyle Barker** | Finance & Client Relations | `relationship-manager` |
| **Dr. Watson** | Wellness & PERMA-V Sage | `wellness` |
| **Regine Hunter** | Social Engineering & Brand | `brand-social` |
| **Scooter** | Travel & Logistics | `travel-logistics` |
| **Overton Wakefield Jones** | Infrastructure & Operations | `infrastructure-ops` |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/TheCraigHewitt/hermes-chief-of-staff.git

# Copy skills to your Hermes installation
cp -r hermes-chief-of-staff/skills/* ~/.hermes/skills/

# Copy workspace files to your project
cp -r hermes-chief-of-staff/workspace/ ~/your-project/workspace/

# Copy and fill out the context file
cp hermes-chief-of-staff/templates/CHIEF_OF_STAFF_CONTEXT.example.md ~/your-project/CHIEF_OF_STAFF_CONTEXT.md

# Set up Khadijah's identity
cp hermes-chief-of-staff/templates/SOUL.example.md ~/.hermes/SOUL.md
```

Then fill in `CHIEF_OF_STAFF_CONTEXT.md` with your details. See [INSTALL.md](INSTALL.md) for the full setup guide.

## The Flavor Protocol

Every request follows the **Editorial Cycle**:

1. **Identification** — Khadijah scans triggers (emails, texts, bank alerts, wellness pings)
2. **Delegation** — Khadijah issues Work Orders to the appropriate specialist
3. **Research & Drafting** — Specialists do the heavy lifting
4. **Synthesis** — Khadijah assembles a "Flavor Brief" — one clear proposal
5. **Human Approval** — You say "Approved," "Modify," or "Reject"
6. **Execution** — Upon approval, Sinclair sends the invite, Kyle makes the payment, or Scooter books the flight

## The Operating Rhythm

1. **2 AM** — Maxine's `daily-task-prep` prepares tomorrow's task list
2. **8 AM** — Khadijah delivers a morning Flavor Brief
3. **All day** — Sinclair sweeps inbox every 15 minutes
4. **Twice daily** — Kyle checks for due follow-ups
5. **End of day** — Khadijah reviews what got done and captures what's next

When nothing needs attention, the system stays silent (`HEARTBEAT_OK`). Every message means something needs your attention.

## Operational Modes

- **Deep Work Mode** — Sinclair silences all agents except Khadijah (emergencies) and Dr. Watson (posture/hydration)
- **Social Mode** — Regine and Kyle take the lead on networking and etiquette prep
- **Recovery Mode** — Dr. Watson and Sinclair lock the calendar; Overton handles all pending bills so you can unplug
- **Standard Mode** — Full staff active

## Choose Your Level

| Level | Skills | What you get |
|-------|--------|-------------|
| **Personal EA** | executive-assistant, daily-task-manager | Inbox triage + task management |
| **Founder** | + relationship-manager, daily-task-prep | + follow-up tracking + daily prep |
| **Full FlavorOS** | + chief-of-staff + all specialists | + morning Flavor Briefs + full staff |

See [docs/maturity-levels.md](docs/maturity-levels.md) for details.

## Configuration

All owner-specific settings live in one file: `CHIEF_OF_STAFF_CONTEXT.md`. Each skill reads this at the start of relevant runs — it's the canonical owner config. No scattered config, no environment variables to manage.

- [templates/CHIEF_OF_STAFF_CONTEXT.example.md](templates/CHIEF_OF_STAFF_CONTEXT.example.md) — Template to fill out
- [templates/CHIEF_OF_STAFF_CONTEXT.demo.md](templates/CHIEF_OF_STAFF_CONTEXT.demo.md) — Filled-out example with fake data

## Docs

- [INSTALL.md](INSTALL.md) — Step-by-step setup guide
- [PHILOSOPHY.md](PHILOSOPHY.md) — Operating principles
- [docs/operating-model.md](docs/operating-model.md) — How the system works end-to-end
- [docs/example-outputs.md](docs/example-outputs.md) — What good output looks like
- [docs/adaptation-guide.md](docs/adaptation-guide.md) — How to customize for your workflow
- [docs/maturity-levels.md](docs/maturity-levels.md) — Personal EA to Full FlavorOS progression
- [cron/README.md](cron/README.md) — Recommended cron schedules

## About

Built by [Craig Hewitt](https://twitter.com/croighewitt). FlavorOS layer by Marcus Bivines. Ported from the [clawchief](https://github.com/snarktank/clawchief) operating model, rebuilt for [Hermes Agent](https://hermes-agent.nousresearch.com/).

## License

MIT
# FlavorOS
