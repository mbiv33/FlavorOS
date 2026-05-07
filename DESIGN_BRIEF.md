# FlavorOS Design Brief

## Product Overview

**FlavorOS** is a multi-agent executive operating system designed for busy professionals. It combines five specialized AI agents that work together to manage communication, operations, logistics, relationships, and strategic planning—with human approval at every critical decision point.

### Core Promise
"Keeping it Professional. Keeping it Flavor." — The system handles identify, research, draft, and organize. The owner handles approve, modify, reject, and act.

## The Five-Agent Team

| Agent | Title | Function | User-Facing? |
|-------|-------|----------|--------------|
| **Khadijah James** | Chief of Staff | Orchestration, briefs, approvals, synthesis | ✓ Primary |
| **Sinclair James** | Executive Assistant | Inbox, calendar, meetings, wellness, voice support | ✓ Direct lane |
| **Maxine Shaw** | COO | Projects, finance ops, business operations | Behind scenes |
| **Scooter** | Chief Logistics | Travel, logistics, IT prep, web research | Behind scenes |
| **Kyle Barker** | CRO | CRM, follow-ups, networking, brand management | Behind scenes |

## User-Facing Surfaces

1. **Khadijah Direct** — Decision briefs, approvals, strategy synthesis
2. **Sinclair Direct** — Daily communications, calendar, wellness check-ins
3. **Shared Group Bot** — Joint conversation space with both Khadijah and Sinclair

## Key Workflows

### Email & Calendar Triage
- Inbound email arrives → system identifies, researches, drafts response
- Calendar conflict → system suggests resolution options
- Meeting prep → system creates prep packet with context

### Project & Task Management
- Owner assigns work → system breaks down, tracks progress, escalates blockers
- Status updates → system synthesizes across agents into executive brief
- Deadline approaching → system surfaces risks and remediation options

### Travel & Logistics
- Travel request → system handles research, booking coordination, prep packets
- Itinerary changes → real-time updates and impact analysis
- Pre-travel → system confirms readiness and flags gaps

### Relationship & Follow-Up Management
- Contact engagement → system tracks cadence and suggests outreach
- Follow-up deadlines → system ensures nothing falls through cracks
- Brand/social positioning → system manages public presence

### Wellness & Well-Being
- Health check-ins → regular pulse on owner's state
- Stress signals → system adjusts workload and offers support
- Recovery time → system protects focus blocks and downtime

## Design Principles

- **Human-in-the-loop**: No money, time commitments, or sensitive relationship moves happen without explicit approval
- **Low-noise by default**: Silence means the system is handling things; only surfacing what needs human input
- **Voice-first interaction**: Natural, conversational primary interface
- **Transparent escalation**: Clear visibility into what each agent is doing and when
- **Artifact generation**: Creates durable outputs (drafts, briefs, task lists, travel packets)

## Information Architecture

### What Users See
- Current context (what just happened, what's next)
- Action items requiring approval
- Generated drafts (email, documents, briefings)
- Status of ongoing workflows
- Wellness and readiness flags

### What Stays Hidden
- Inter-agent coordination and specialist work
- Failed attempts or research dead-ends
- Routine processing (unless escalated)
- Backend system state

## Tone & Voice

- Professional but not stiff
- Proactive without being pushy
- Confident but consultative
- Respectful of owner's time and decision-making authority
- Culturally grounded with personality

## Voice-First Experience

FlavorOS is **voice-forward**, not voice-optional. The UI is designed around natural conversation as the primary input method:

- **Continuous listening** — the system is always ready to receive voice input
- **Real-time transcription** — spoken words appear on screen as you speak
- **Voice visual feedback** — waveforms, speaking indicators, listening state
- **Speaker identification** — in group conversations, clear visual markers show who's speaking (Khadijah vs. Sinclair)
- **Haptic + audio cues** — system acknowledgment and state changes via sound/touch
- **Voice-optimized replies** — quick-tap buttons for common responses alongside typed input

The UI doesn't *support* voice—it *centers* voice, with text and visual context as supporting elements.

## Technical Context

- Voice-forward with Gemini/Twilio integration
- Runs on containerized VPS infrastructure
- Obsidian vault for institutional memory
- NATS messaging bus for inter-agent coordination
- Multi-account support (multiple emails, calendars, platforms)

## Design Goals

1. Make invisible work visible (help owner understand what system is doing)
2. Minimize cognitive load (clear prioritization, no noise)
3. Feel like a real team (not a single chatbot)
4. Preserve executive autonomy (approve/modify/reject every move)
5. Create durable institutional memory (artifacts live beyond the conversation)
