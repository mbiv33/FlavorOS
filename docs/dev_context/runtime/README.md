# Runtime Dev-Agent Reports

This folder is the scratch reporting lane for temporary VPS development agents.

These agents are not product agents. They exist only to accelerate FlavorOS launch work and must not contaminate the canonical five-agent product identity.

## Files

- `agent1-logwatch.md`: compose, logs, syntax checks, and no-value health checks.
- `agent2-provider-research.md`: official provider/API research and implementation notes.
- `agent3-endpoint-tests.md`: synthetic endpoint and NATS test results using fake data.

## Rules

- Do not print or store secret values.
- Do not use real client data.
- Do not send emails, SMS, calendar invites, public posts, bookings, or payments.
- Report commands, pass/fail status, paths, error classes, and recommended fixes only.
- Promote durable findings into project docs only after Khadijah or Maxine accepts the report.

