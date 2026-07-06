"""Security guardrails for Garrafeira Bali (course concept: Security features).

Why a guardrail and not just prompt instructions? Instructions ask the model
to behave; a guardrail *forces* it. This callback runs BEFORE any tool
executes (deterministic Python, outside the LLM), so even if the model is
tricked or hallucinates, a non-compliant order physically cannot reach the
order book. This mirrors the Day 4 lesson: put policy in code, not in hope.

Policies enforced on `place_order`:
  1. Age gate      - customer must have confirmed being 21+ (Indonesian law).
  2. Quantity cap  - 1 to 12 bottles per order (anti-abuse / retail licence).
  3. Input hygiene - types and values validated before touching business data.

Returning a dict from a before_tool_callback SKIPS the real tool call and
uses that dict as the tool's result - i.e. the order is blocked and the
agent must relay the refusal to the customer. Returning None lets the
tool run normally.
"""

from typing import Any, Optional

from google.adk.tools.base_tool import BaseTool

MAX_BOTTLES_PER_ORDER = 12


def _blocked(reason: str) -> dict:
    """Standard shape for a blocked call, so the agent can explain it."""
    return {"status": "blocked_by_guardrail", "reason": reason}


def order_guardrail(
    tool: BaseTool, args: dict[str, Any], context: Any
) -> Optional[dict]:
    """Inspect every tool call made by the order desk; veto unsafe orders."""
    if tool.name != "place_order":
        return None  # Other tools (e.g. check_stock) pass through untouched.

    # --- Policy 1: age verification (legal drinking age in Indonesia: 21) ---
    if args.get("customer_is_21_plus") is not True:
        return _blocked(
            "Order refused: the customer has not confirmed being 21 or older. "
            "Politely ask for age confirmation before ordering."
        )

    # --- Policy 2 & 3: quantity must be a sane integer within the cap ------
    quantity = args.get("quantity")
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return _blocked("Order refused: quantity must be a whole number.")
    if quantity < 1:
        return _blocked("Order refused: quantity must be at least 1 bottle.")
    if quantity > MAX_BOTTLES_PER_ORDER:
        return _blocked(
            f"Order refused: maximum {MAX_BOTTLES_PER_ORDER} bottles per "
            "order. Suggest the customer split large purchases or contact "
            "the owner directly for a case order."
        )

    # --- Policy 3 continued: required text fields must not be empty --------
    for field in ("customer_name", "delivery_area", "wine_id"):
        value = args.get(field)
        if not isinstance(value, str) or not value.strip():
            return _blocked(f"Order refused: '{field}' is missing or empty.")

    return None  # All policies satisfied: allow the real tool to execute.
