"""Business tools for Garrafeira Bali.

Design note: each tool is a plain, typed Python function. ADK reads the type
hints and docstrings to build the tool schema automatically, so the agent
knows exactly what arguments each tool expects. All tools return a dict with
a "status" key ("success" or "error") so the agent can reason about failures.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CATALOG_FILE = DATA_DIR / "catalog.json"
INVENTORY_FILE = DATA_DIR / "inventory.json"
ORDERS_FILE = DATA_DIR / "orders.json"

# Delivery areas the shop currently serves (kept small on purpose).
DELIVERY_AREAS = ["canggu", "seminyak", "ubud", "uluwatu", "denpasar", "sanur"]


def _load_json(path: Path, default):
    """Read a JSON file, returning a default value if it does not exist."""
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_catalog() -> dict:
    """Return the full wine catalog: the 3 Portuguese wines the shop sells.

    Use this to recommend wines, answer questions about taste, food pairing,
    region, or price. Prices are in Indonesian Rupiah (IDR).

    Returns:
        dict: status plus the list of wines with id, name, style, tasting
        notes, food pairing and price.
    """
    catalog = _load_json(CATALOG_FILE, {"wines": []})
    return {"status": "success", "catalog": catalog}


def check_stock(wine_id: str) -> dict:
    """Check how many bottles of a given wine are currently in stock.

    Args:
        wine_id: The wine identifier, e.g. "VV-001", "DR-002" or "PT-003".

    Returns:
        dict: status, wine_id and bottles_in_stock (or an error message
        if the wine_id is unknown).
    """
    inventory = _load_json(INVENTORY_FILE, {})
    wine_id = wine_id.strip().upper()
    if wine_id not in inventory:
        return {"status": "error", "message": f"Unknown wine_id '{wine_id}'."}
    return {
        "status": "success",
        "wine_id": wine_id,
        "bottles_in_stock": inventory[wine_id],
    }


def place_order(
    wine_id: str,
    quantity: int,
    customer_name: str,
    delivery_area: str,
    customer_is_21_plus: bool,
) -> dict:
    """Place a customer order and decrement stock.

    IMPORTANT: only call this after the customer has explicitly confirmed
    the wine, the quantity, their delivery area, and that they are 21 or
    older (the legal drinking age in Indonesia). A security guardrail
    inspects every call to this tool and will block non-compliant orders.

    Args:
        wine_id: The wine identifier, e.g. "VV-001".
        quantity: Number of bottles (1 to 12 per order).
        customer_name: Name for the delivery.
        delivery_area: One of the served areas in Bali, e.g. "Canggu".
        customer_is_21_plus: True only if the customer confirmed being 21+.

    Returns:
        dict: status and, on success, an order confirmation with order_id,
        total price in IDR, and remaining stock.
    """
    inventory = _load_json(INVENTORY_FILE, {})
    catalog = _load_json(CATALOG_FILE, {"wines": []})
    wine_id = wine_id.strip().upper()

    wine = next((w for w in catalog["wines"] if w["wine_id"] == wine_id), None)
    if wine is None:
        return {"status": "error", "message": f"Unknown wine_id '{wine_id}'."}

    area = delivery_area.strip().lower()
    if area not in DELIVERY_AREAS:
        return {
            "status": "error",
            "message": (
                f"Sorry, we do not deliver to '{delivery_area}' yet. "
                f"Served areas: {', '.join(a.title() for a in DELIVERY_AREAS)}."
            ),
        }

    in_stock = inventory.get(wine_id, 0)
    if quantity > in_stock:
        return {
            "status": "error",
            "message": f"Only {in_stock} bottles of {wine['name']} left in stock.",
        }

    # Commit the order: decrement stock and append to the order book.
    inventory[wine_id] = in_stock - quantity
    _save_json(INVENTORY_FILE, inventory)

    order = {
        "order_id": f"GB-{uuid.uuid4().hex[:8].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "wine_id": wine_id,
        "wine_name": wine["name"],
        "quantity": quantity,
        "unit_price_idr": wine["price_idr"],
        "total_idr": wine["price_idr"] * quantity,
        "customer_name": customer_name.strip(),
        "delivery_area": area.title(),
        "age_verified": customer_is_21_plus,
    }
    orders = _load_json(ORDERS_FILE, [])
    orders.append(order)
    _save_json(ORDERS_FILE, orders)

    return {
        "status": "success",
        "confirmation": order,
        "remaining_stock": inventory[wine_id],
    }
