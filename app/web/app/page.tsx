import { MOCK_USER } from "@/lib/mock/profile";

/**
 * Today — calm-state placeholder for Slice 1. Surface gets fully built in
 * Slice 3 (greeting, Ready-for-you, brief, briefing agenda, agenda strip,
 * trips, quietly handled).
 *
 * Per PRD principle 2: when nothing's pending, the page stays short.
 */
export default function TodayPage() {
  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  return (
    <div>
      <div className="px-1 pt-4 pb-1.5">
        <h1 className="m-0 mb-1 text-[28px] font-bold tracking-tight">
          {greeting}, {MOCK_USER.firstName}.
        </h1>
        <div className="text-[13.5px] text-ink-2">
          Nothing needs you yet. Khadijah is putting your day together.
        </div>
      </div>
    </div>
  );
}
