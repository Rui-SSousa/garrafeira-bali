# VIDEO SCRIPT — 5 minutes max (rubric: 10 points)

Record your screen + voice. Two windows ready before recording:
(A) Antigravity with the project open, (B) a terminal running `adk web`
with the browser on http://localhost:8000, and the file
`garrafeira/data/inventory.json` visible in a split pane.

The rubric explicitly rewards: Problem → Why agents → Architecture →
Demo → The Build. The script follows exactly that order.

---

## [0:00–0:35] Problem statement

> "Hi, I'm Rui. This is Garrafeira Bali — a one-person online business
> selling three Portuguese wines in Bali. For a solo founder, every sale
> is the same chat: recommend a wine, answer pairing questions, check
> stock, verify the customer is over 21 — the legal drinking age in
> Indonesia — cap the order at twelve bottles, and log the delivery.
> None of it is hard. All of it is constant. And the shop stops the
> moment the founder sleeps."

*(Show: the shop's catalog.json with the 3 wines on screen.)*

## [0:35–1:05] Why agents?

> "A web form can take orders but can't advise. A chatbot can advise
> but can't be trusted to act — it'll hallucinate discounts or sell to
> a minor. This business needs both a natural conversation AND hard,
> non-negotiable rules around real actions. That's exactly the agent
> pattern from this course: an LLM for the conversation, tools for the
> actions, and deterministic guardrails for the rules."

## [1:05–1:50] Architecture

*(Show: the mermaid diagram in the README.)*

> "The shop is a team of three ADK agents — like three employees.
> The Concierge is the root agent: it greets and routes. The Sommelier
> recommends wines, always reading from the catalog tool, never from
> imagination. The Order Desk checks stock and places orders — but
> every order passes through a security guardrail first: a
> before_tool_callback in plain Python that vetoes any order without
> an explicit 21-plus confirmation, over twelve bottles, or with
> malformed input. The model decides what to say; code decides what
> is allowed."

## [1:50–3:50] Demo (the heart of the video)

*(Switch to `adk web`. Keep inventory.json visible.)*

1. Type: **"Something light for grilled seafood on a hot afternoon?"**
   > "The concierge transfers to the sommelier — you can see the agent
   > transfer here — and it recommends the Vinho Verde, with the price
   > in rupiah, straight from the catalog."
2. Type: **"Great, 2 bottles. I'm Rui, delivery to Canggu, and yes, I'm over 21."**
   > "Now the order desk takes over: it checks stock, confirms the
   > total, and places the order. Watch inventory.json — stock just
   > dropped from 24 to 22, and the order is in the order book."
3. Type: **"Actually, make it 50 bottles."**
   > "The model tried to call place_order — and the guardrail blocked
   > it before it executed. The agent explains the 12-bottle policy.
   > This isn't the model being polite; the tool call was physically
   > vetoed by code."
4. (Optional if time) Start a new order and refuse to confirm age:
   > "Same story with age: no explicit 21-plus confirmation, no sale.
   > Even a prompt injection can't reach the order book."

## [3:50–4:40] The build

*(Switch to Antigravity: show SKILL.md and a prompt/plan from the session.)*

> "I vibe-coded the whole project in Google Antigravity. My workflow:
> first I wrote a domain skill — SKILL.md — with the business facts and
> compliance rules, so every session started with the same context
> instead of me re-explaining the shop each time. Then one prompt
> scaffolded the three-agent team, and I reviewed and tightened each
> instruction. The tools are simple typed Python functions; the one
> file I tested exhaustively by hand, without the LLM, is the
> guardrail — deterministic policy deserves deterministic tests."

## [4:40–5:00] Close

> "Three wines, three agents, three tools, one guardrail — a complete
> business loop in about 300 lines of Python, that never invents a
> product and provably can't make an illegal sale. Code and setup
> instructions are on GitHub, linked in the writeup. Thanks!"

---

### Recording tips
- 1080p, system font size up, dark theme reads well on YouTube.
- Do a dry run of the demo once first — then reset `inventory.json`
  to 24/18/12 and delete `orders.json` so the on-camera run shows the
  clean 24 → 22 stock change.
- Upload as **Public** or **Unlisted** on YouTube (judges must reach it
  without login). Verify the link in an incognito window.
