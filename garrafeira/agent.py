"""Garrafeira Bali - a multi-agent AI storefront (course concept: ADK multi-agent).

Think of a tiny wine shop with three employees:

  - The CONCIERGE greets you at the door and decides who should help you.
  - The SOMMELIER knows the 3 wines by heart and recommends the right one.
  - The ORDER DESK checks the shelf, takes your order, and (crucially) is
    supervised by a security guardrail that vetoes any non-compliant sale.

In ADK terms: a root LlmAgent with two specialised sub-agents. The root
agent transfers the conversation to whichever specialist fits the request,
which keeps each agent's instructions short, focused and testable.

The model is configurable via the GARRAFEIRA_MODEL environment variable so
the project keeps working as new Gemini versions ship.
"""

import os

from google.adk.agents import Agent

from .guardrails import order_guardrail
from .tools import check_stock, get_catalog, place_order

MODEL = os.getenv("GARRAFEIRA_MODEL", "gemini-2.5-flash")

# --------------------------------------------------------------------------
# Specialist 1: the sommelier - recommendations, pairing, product questions.
# --------------------------------------------------------------------------
sommelier = Agent(
    name="sommelier",
    model=MODEL,
    description=(
        "Portuguese wine expert. Handles recommendations, taste questions, "
        "food pairing and prices for the 3 wines in the catalog."
    ),
    instruction=(
        "You are the sommelier of Garrafeira Bali, a small online shop in "
        "Bali selling exactly 3 Portuguese wines. Always call get_catalog "
        "first; never invent wines, prices or stock. Recommend at most one "
        "or two wines, matched to the customer's taste, food or budget "
        "(prices are in IDR). Mention local Bali food pairings when natural. "
        "Be warm and concise - two short paragraphs maximum. If the customer "
        "wants to buy, transfer them to the order_desk agent."
    ),
    tools=[get_catalog],
)

# --------------------------------------------------------------------------
# Specialist 2: the order desk - stock checks and order placement,
# supervised by the security guardrail (before_tool_callback).
# --------------------------------------------------------------------------
order_desk = Agent(
    name="order_desk",
    model=MODEL,
    description=(
        "Handles stock availability checks and places customer orders "
        "for delivery within Bali."
    ),
    instruction=(
        "You are the order desk of Garrafeira Bali. Before placing any "
        "order you MUST collect and confirm: (1) the wine_id, (2) quantity "
        "(max 12 bottles), (3) the customer's name, (4) delivery area in "
        "Bali, and (5) an explicit confirmation that the customer is 21 or "
        "older - the legal drinking age in Indonesia. Check stock with "
        "check_stock before promising anything. Summarise the order and "
        "total price in IDR and get a clear 'yes' from the customer before "
        "calling place_order. If a guardrail blocks the order, apologise "
        "and explain the policy honestly. Never work around the guardrail."
    ),
    tools=[check_stock, place_order],
    before_tool_callback=order_guardrail,
)

# --------------------------------------------------------------------------
# Root agent: the concierge - routes each request to the right specialist.
# --------------------------------------------------------------------------
root_agent = Agent(
    name="garrafeira_concierge",
    model=MODEL,
    description="Front door of Garrafeira Bali, an online Portuguese wine shop in Bali.",
    instruction=(
        "You are the friendly concierge of Garrafeira Bali, a one-person "
        "online shop selling 3 Portuguese wines with delivery across "
        "southern Bali. Greet customers briefly. Route wine advice, taste "
        "and pairing questions to the sommelier agent; route stock checks "
        "and purchases to the order_desk agent. Answer only shop-related "
        "questions; politely decline anything else. Keep replies short."
    ),
    sub_agents=[sommelier, order_desk],
)
