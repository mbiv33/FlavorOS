import { cn } from "@/lib/cn";

/**
 * Right rail container — three threads + voice orb + composer.
 * Always present except during the Call Surface (which takes over the rail).
 *
 * Slice 1: container shell only. Threads, composer, voice are filled in
 * Slice 5 along with the Call Surface.
 */
export function RightRail() {
  return (
    <aside
      className={cn(
        "self-start sticky top-[76px]",
        "h-[calc(100vh-96px)]",
        "flex flex-col overflow-hidden",
        "bg-card border border-line rounded-[18px] backdrop-blur-md shadow-sm2",
      )}
      aria-label="Persistent chat"
    >
      <div className="px-4 py-3 border-b border-line text-[12px] text-ink-3 font-semibold uppercase tracking-[0.06em]">
        Persistent chat
      </div>

      <div className="flex-1 overflow-auto p-2 flex flex-col gap-2">
        {/* Threads list — populated in Slice 5. */}
      </div>

      <div className="border-t border-line p-2.5 bg-[rgba(255,255,255,0.6)]">
        <div className="w-full flex items-center gap-2.5 px-3 py-2 bg-card-solid border border-line rounded-full text-ink-3 text-[12.5px] mb-2">
          <span
            aria-hidden
            className="w-[22px] h-[22px] rounded-full bg-gradient-to-br from-kha to-kyl shadow-[0_0_0_2px_rgba(91,70,214,0.1)]"
          />
          Voice idle
          <span className="ml-auto">
            <span className="kbd">space</span> to talk
          </span>
        </div>
        <div className="flex items-center gap-1.5 bg-card-solid border border-line rounded-xl px-2.5 py-2">
          <input
            placeholder="Type a message…"
            aria-label="Compose message"
            className="flex-1 bg-transparent border-0 outline-none font-sans text-[13px] text-ink placeholder:text-ink-3"
          />
          <button
            type="button"
            aria-label="Send"
            className="w-[26px] h-[26px] rounded-full bg-ink text-white grid place-items-center text-[11px]"
          >
            ↑
          </button>
        </div>
      </div>
    </aside>
  );
}
