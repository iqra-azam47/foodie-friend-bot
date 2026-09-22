"""Loads the menu from data/menu.json and gives simple helpers to use it."""
import json

from config import MENU_FILE

with open(MENU_FILE, encoding="utf-8") as file:
    MENU = json.load(file)


def _build_price_list(menu):
    """One flat list: {'Zinger Burger': 450, 'Pepperoni Pizza (Large)': 1900, ...}"""
    prices = {}
    for items in menu.values():
        for name, value in items.items():
            if isinstance(value, dict):  # an item that comes in sizes
                for size, price in value.items():
                    prices[f"{name} ({size})"] = price
            else:
                prices[name] = value
    return prices


PRICES = _build_price_list(MENU)


def find_item(text):
    """Find the exact menu name for what the customer typed.
    Returns None if nothing matches, or if more than one item matches (for example just 'pizza')."""
    wanted = (text or "").strip().lower()
    if not wanted:
        return None
    for name in PRICES:
        if name.lower() == wanted:
            return name
    matches = [name for name in PRICES if wanted in name.lower()]
    return matches[0] if len(matches) == 1 else None


def format_menu():
    """The menu as easy-to-read text for the AI instructions."""
    lines = []
    for category, items in MENU.items():
        lines.append(f"{category}:")
        for name, value in items.items():
            if isinstance(value, dict):
                sizes = ", ".join(f"{size} Rs. {price}" for size, price in value.items())
                lines.append(f"- {name}: {sizes}")
            else:
                lines.append(f"- {name}: Rs. {value}")
        lines.append("")
    return "\n".join(lines).strip()
