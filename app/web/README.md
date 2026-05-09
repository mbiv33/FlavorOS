# FlavorOS Web

Front-end web app implementing the [FlavorOS UI PRD](../../docs/prd/ui/README.md).

## Run

```bash
cd app/web
npm install
npm run dev
```

Then open <http://localhost:3000>.

## Stack

- Next.js 14 (app router) · React 18 · TypeScript strict
- Tailwind CSS, fed by CSS custom properties in `styles/tokens.css`
- Radix Primitives for accessible interactions
- Zustand for cross-surface client state (Approval Card sync, voice state)
- Framer Motion for the few animations (orb pulse, card transitions)
- cmdk for the ⌘K palette

## Folder map

```
app/                  Next routes — Today, Work, Travel, Messages, Calendar, Library, Preferences
components/
  shell/              Header, LeftNav, RightRail, ContextSelector
  primitives/         Avatar, Chip, Button, Card, Section
  approval/           ApprovalCard + Modify subform + Ripple panel  (Slice 2)
  today/ work/ ...    Per-surface composition                       (Slice 3+)
  call/               Call Surface                                  (Slice 5)
  palette/            ⌘K                                            (Slice 5)
  voice/              Orb states + voice-phrase mapper              (Slice 5)
lib/
  types/              Type contracts mirroring backend shapes
  mock/               Mock data layer — single-file swap to real fetch
  state/              Zustand stores                                (Slice 2+)
  voice/              Voice phrase → action stub                   (Slice 5)
styles/
  tokens.css          Color/space/radius tokens (light + dark)
  globals.css
```

## Design principles

Read [`docs/prd/ui/00-principles-and-vocabulary.md`](../../docs/prd/ui/00-principles-and-vocabulary.md) before
adding components. The non-negotiables:

1. Sausage > sausage-making — never expose backend mechanics
2. Silence equals working — empty states render nothing, not placeholders
3. Voice-first — every action has a voice phrase
4. Context-agnostic — never hardcode context labels; selector hidden if 1 context
5. One canonical decision component — Approval Card

## Theming

All color/radius/shadow values are CSS custom properties in `styles/tokens.css`.
Dark mode is class-based (`.dark` on `<html>`) and uses the same property names
with different values. To restyle, edit tokens — components shouldn't need to change.

## Single-context test

Set `NEXT_PUBLIC_FLAVOROS_SINGLE_CONTEXT=1` to verify the "zero context-switching
chrome" rule (header context selector hidden, context chips suppressed).
