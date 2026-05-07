# Claude Design Prompt for FlavorOS UI

Copy and paste this into Claude Design, then customize the final section based on what screens you want.

---

## **Design Brief**

You are designing the UI for **FlavorOS**, a voice-first, multi-agent executive assistant system.

### What is FlavorOS?
FlavorOS is a five-agent operating system where specialized AI agents (Chief of Staff, Executive Assistant, COO, Logistics Officer, CRO) coordinate to manage the owner's email, calendar, projects, travel, relationships, and wellness. The system operates on one principle: **System handles identify, research, draft, organize. Owner handles approve, modify, reject, act.**

### Voice is Primary, Not Secondary
FlavorOS is **voice-forward**. The owner primarily speaks to the system. The visual UI is designed to *support and enhance* the voice experience, not replace it.

- The system is always listening and ready
- Spoken words appear as real-time transcripts
- Voice state is always visible (listening, processing, speaking)
- Responses come via voice + supporting visual context
- Text input is available but secondary to voice

### User-Facing Surfaces

**1. Khadijah Direct** — Chief of Staff
- Decision briefs, strategic approvals, synthesis
- Owner initiates voice conversation; Khadijah responds
- High-information-density context (briefing materials, options, recommendations)

**2. Sinclair Direct** — Executive Assistant  
- Daily comms triage, calendar, wellness, task updates
- Natural back-and-forth voice conversation
- Lower cognitive overhead; supportive tone

**3. Shared Group Bot** — Khadijah + Sinclair Together
- Multi-speaker conversation (3-way: owner, Khadijah, Sinclair)
- Clear visual speaker identification ("Khadijah responds", "Sinclair adds")
- Coordinated agent handoff and tag-team handling

---

## **Core Design Elements**

### Voice Interaction Display
Must show in every screen:

1. **Listening State**
   - Waveform animation (input levels, real-time)
   - "Listening..." indicator with pulsing visual
   - Mic on/off toggle with clear status

2. **Real-Time Transcript**
   - Owner's speech appears live as they speak
   - System responses appear as voice is playing
   - Transcript history scrollable below current exchange

3. **Speaker Identity**
   - Color-coded or icon-based speaker labels (Khadijah, Sinclair, Owner)
   - In group conversations: clear visual separation between who's speaking
   - Voice waveform color matches speaker identity

4. **System State**
   - "Processing..." when system is thinking
   - "Speaking..." when agent is responding (with waveform)
   - "Complete" or ready state after response finishes

5. **Voice Feedback**
   - Subtle audio chime when system is ready
   - Visual confirmation when voice input is recognized
   - Haptic feedback on mobile (if applicable)

### Context Display (Secondary)
Visible but not dominant:

- **Current priorities** (what's urgent, what needs approval)
- **Recent context** (last email, next meeting, current project)
- **Pending actions** (what's awaiting owner decision)
- **Generated artifacts** (drafts, briefings, task lists—swipeable or slide-in)

### Quick-Reply Layer
Voice-optimized quick actions:

- "Approve", "Modify", "Reject" buttons for decisions
- "Send that", "Save as draft" for generated work
- "Schedule that" for calendar items
- "Add to follow-ups" for relationship actions

These buttons integrate naturally with voice flow—owner can tap or say the action.

---

## **Design Flows to Show**

### Flow 1: Voice Conversation with Context
Owner speaks a request → Real-time transcript appears → System thinks → Agent responds via voice → Response transcript + supporting context cards appear below

### Flow 2: Group Chat Speaker Identification  
Three-way conversation where you clearly see who's speaking at each moment (waveform + speaker name + color coding)

### Flow 3: Decision Approval from Voice
Agent proposes action verbally → Transcript + visual preview appears → Owner approves/modifies/rejects via voice or quick-tap button → System confirms

### Flow 4: Artifact Generation & Review
System generates draft email (during voice conversation) → Transcript continues → Draft card appears in-viewport → Owner reviews, requests changes, or approves—all via voice

### Flow 5: Multi-Agent Handoff
Owner asks Sinclair something → Sinclair coordinates with Maxine behind scenes → Sinclair returns with answer (voice + context cards) → Clear visual indication that other agents were involved

---

## **Visual & Interaction Principles**

1. **Voice State Always Visible** — waveforms, listening indicators, speaker labels are permanently on-screen
2. **Transcript is History** — scroll history builds naturally below the active conversation
3. **Asynchronous Artifact Flow** — drafts/context cards appear inline without disrupting voice conversation
4. **Minimal Text Friction** — text input exists but is recessed; voice is the path of least resistance
5. **Color Coding** — consistent use of color/icon for each agent (Khadijah, Sinclair, Owner, System state)
6. **Generous Whitespace** — voice UI benefits from breathing room; don't clutter
7. **Haptic + Audio Feedback** — reinforce voice interaction with sound and touch (on mobile)

---

## **Example Information Hierarchy**

### 1. Active Voice (Center, Large)
- Current speaker waveform + transcript
- Listening or speaking indicator
- Real-time processing state

### 2. Recent Exchange (Above)
- Previous turns in conversation
- Speaker-labeled transcript history
- Scrollable up to see older context

### 3. Supporting Context (Right sidebar or slide-in panel)
- Priority list, calendar next item, recent email
- Generated drafts/artifacts
- Status of ongoing workflows

### 4. Quick Actions (Bottom or overlay)
- Approve/Modify/Reject buttons
- Common voice commands as tappable buttons
- Text input field (recessed)

---

## **Device Considerations**

- **Mobile First** — Owner is likely moving; voice interaction is perfect for this
- **iPad/Tablet** — larger screen can show more context; still voice-primary
- **Desktop** — can have richer context panels alongside primary voice chat

---

## **Brand Tone**

Professional, confident, grounded. Think executive assistant, not chatbot. 

- Clear, no fluff
- Respectful of owner's authority and time
- Proactive without being pushy
- Culturally grounded with personality
- Visual identity supports voice (not text-heavy)

---

## **What to Design**

Please create **[number]** **[fidelity level]** screens showing:

**Examples:**
- "4 wireframes showing: (1) Sinclair direct morning triage with voice + email context, (2) Khadijah group bot with 3-way conversation and speaker ID, (3) Decision approval flow (voice → transcript → decision button), (4) Mobile listening state with waveform"

- "3 high-fidelity mockups of voice-first interfaces: desktop Khadijah brief, mobile Sinclair direct, and group bot speaker-identification example"

- "Design the active listening state and transcript flow for a 2-minute voice conversation between owner and Khadijah, showing real-time transcript, speaker labels, and artifact cards appearing inline"

---

**Replace the "What to Design" section above with your specific request, then paste into Claude Design.**
