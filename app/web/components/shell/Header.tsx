import Link from "next/link";
import { ContextSelector } from "./ContextSelector";
import { getContexts } from "@/lib/mock/profile";

/**
 * Sticky header. 8 slots per PRD 02 §Header strip.
 * Slot 7 (system alert) only renders when something is wrong — left out
 * entirely until alerts wire up.
 * Slots 4–6 stubbed with sensible defaults; counts come from real stores
 * in later slices.
 */
export function Header() {
  const contexts = getContexts();

  return (
    <header className="glass sticky top-0 z-40 border-b border-line">
      <div
        className="grid items-center gap-6 px-7 py-3.5"
        style={{ gridTemplateColumns: "260px 1fr auto" }}
      >
        {/* Slot 1 — Wordmark */}
        <Link href="/" className="flex items-center gap-2 no-underline text-ink">
          <span
            aria-hidden
            className="w-2.5 h-2.5 rounded-full bg-gradient-to-br from-kha to-kyl"
          />
          <span className="font-extrabold text-[17px] tracking-tight">
            Flavor<span className="text-ink-3 font-bold">OS</span>
          </span>
        </Link>

        {/* Slots 2 + 3 — Context selector + next-event line */}
        <div className="flex items-center gap-3.5 min-w-0">
          <ContextSelector contexts={contexts} />
          <NextEventLine />
        </div>

        {/* Slots 4–6 + 8 — wellness, needs-you, voice, ⌘K */}
        <div className="flex items-center gap-2">
          <WellnessChip />
          <NeedsYouChip />
          <VoiceChip />
          <CommandKChip />
        </div>
      </div>
    </header>
  );
}

function NextEventLine() {
  // Stub — will read from calendar store in Slice 3.
  return (
    <span className="text-[13.5px] text-ink-2 truncate">
      Next: <strong className="text-ink font-semibold">10am NTC standup</strong>
      {" "}— in 24 min
    </span>
  );
}

function HChip({
  variant = "default",
  children,
  ariaLabel,
}: {
  variant?: "default" | "urgent" | "voiceLive";
  children: React.ReactNode;
  ariaLabel?: string;
}) {
  const styles =
    variant === "urgent"
      ? "bg-[rgba(91,70,214,0.07)] text-accent border-[rgba(91,70,214,0.2)]"
      : variant === "voiceLive"
        ? "bg-[rgba(196,99,46,0.08)] text-warn border-[rgba(196,99,46,0.2)]"
        : "bg-card-solid text-ink-2 border-line hover:border-line-2";
  return (
    <button
      type="button"
      aria-label={ariaLabel}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full border text-[12.5px] font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60 ${styles}`}
    >
      {children}
    </button>
  );
}

function WellnessChip() {
  // Slot 4 — ambient indicator. Steady = ok dot. Pulse animation added when stress is elevated.
  return (
    <HChip ariaLabel="Wellness: steady">
      <span className="w-[7px] h-[7px] rounded-full bg-ok" aria-hidden />
      steady
    </HChip>
  );
}

function NeedsYouChip() {
  // Slot 5 — count of pending Approval cards. Hidden when zero.
  // Stubbed at 1 for now; wired to approvals store in Slice 2.
  const pending = 1;
  if (pending === 0) return null;
  return (
    <HChip variant="urgent" ariaLabel={`${pending} ready for you`}>
      <span className="w-[7px] h-[7px] rounded-full bg-accent animate-pulse" aria-hidden />
      {pending} ready for you
    </HChip>
  );
}

function VoiceChip() {
  // Slot 6 — voice state. Idle / listening / processing / live-call.
  return (
    <HChip ariaLabel="Voice idle">
      <span className="w-[7px] h-[7px] rounded-full bg-ink-3" aria-hidden />
      Voice idle
    </HChip>
  );
}

function CommandKChip() {
  return (
    <HChip ariaLabel="Open command palette">
      <span className="kbd">⌘K</span>
    </HChip>
  );
}
