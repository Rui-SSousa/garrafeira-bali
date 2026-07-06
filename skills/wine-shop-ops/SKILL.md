---
name: wine-shop-ops
description: Domain skill for operating Garrafeira Bali, a 3-product online Portuguese wine shop in Bali. Use whenever generating, reviewing, or extending code or agent instructions for this shop - it encodes the catalog rules, compliance policies, and tone that every agent and tool must respect.
---

# Wine Shop Operations Skill

This skill was used inside Antigravity (Agents CLI workflow) during
development so that every vibe-coding session started from the same
business rules instead of re-explaining them in each prompt.

## Business facts (single source of truth)

- The shop sells exactly **3 wines**; product data lives in
  `garrafeira/data/catalog.json`. Never hardcode wines, prices, or stock
  in prompts or code - always read the catalog.
- Prices are in **IDR**. Stock lives in `garrafeira/data/inventory.json`;
  orders are appended to `garrafeira/data/orders.json`.
- Delivery is limited to: Canggu, Seminyak, Ubud, Uluwatu, Denpasar, Sanur.

## Compliance policies (non-negotiable)

1. Legal drinking age in Indonesia is **21**. No order proceeds without an
   explicit customer confirmation of being 21+.
2. Maximum **12 bottles per order**.
3. These policies must be enforced in **deterministic code**
   (`garrafeira/guardrails.py`), not only in agent instructions.
4. Secrets (API keys) live only in `.env`, never in source code.

## Architecture conventions

- One root `concierge` agent that routes; specialists do the work:
  `sommelier` (advice) and `order_desk` (stock + orders).
- Every tool returns a dict with a `"status"` key so agents can reason
  about errors instead of crashing.
- Keep agent instructions short and specific; put policy in guardrails.

## Tone

Warm, brief, honest. Recommend at most 1-2 wines. Mention Bali food
pairings (seafood nasi goreng, babi guling) where natural. Politely refuse
anything unrelated to the shop.
