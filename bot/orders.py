"""The order system. The AI asks for things, but THIS code checks the menu,
does the math, checks the phone number and locks a placed order."""
import re
from datetime import datetime

from bot.menu import PRICES, find_item
from config import DELIVERY_AREA, DELIVERY_FEE, DELIVERY_TIME, MAX_ITEM_QUANTITY


def clean_phone(phone):
    """Accept 03001234567, +923001234567 or 923001234567.
    Returns the number as 03001234567, or None if it is not a valid Pakistani mobile number."""
    digits = re.sub(r"[\s\-()]", "", phone or "")
    match = re.fullmatch(r"(?:\+92|92|0)(3\d{9})", digits)
    return "0" + match.group(1) if match else None


def new_order_state():
    """An empty order. This small dictionary is what we keep in the session."""
    return {"cart": {}, "pending": None, "locked": False}


class OrderTools:
    """The methods below are the 'tools' the AI is allowed to call."""

    def __init__(self, state):
        self.cart = dict(state["cart"])
        self.pending = state["pending"]
        self.locked = state["locked"]

    def get_state(self):
        return {"cart": self.cart, "pending": self.pending, "locked": self.locked}

    def _bill(self):
        items = []
        subtotal = 0
        for name, quantity in self.cart.items():
            line_total = PRICES[name] * quantity
            items.append({"item": name, "quantity": quantity,
                          "price_each": PRICES[name], "line_total": line_total})
            subtotal += line_total
        return {"items": items, "subtotal": subtotal,
                "delivery_fee": DELIVERY_FEE, "total": subtotal + DELIVERY_FEE}

    def add_to_cart(self, item_name: str, quantity: int = 1) -> dict:
        """Add a menu item to the customer's cart. Use the exact menu name.
        Pizza names include the size, for example 'Pepperoni Pizza (Large)'."""
        if self.locked:
            return {"error": "This order is already placed. If the customer wants "
                             "another order, call start_new_order first."}
        name = find_item(item_name)
        if name is None:
            wanted = (item_name or "").strip().lower()
            similar = [n for n in PRICES if wanted and wanted in n.lower()]
            return {"error": "Item not found on the menu (or the name matches more than one item).",
                    "did_you_mean": similar[:6]}
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 0
        if not 1 <= quantity <= MAX_ITEM_QUANTITY or self.cart.get(name, 0) + quantity > MAX_ITEM_QUANTITY:
            return {"error": f"Quantity must be between 1 and {MAX_ITEM_QUANTITY} for each item."}
        self.cart[name] = self.cart.get(name, 0) + quantity
        self.pending = None  # the cart changed, so the receipt must be made again
        return {"added": name, "quantity": quantity, "cart": self._bill()}

    def remove_from_cart(self, item_name: str) -> dict:
        """Remove an item completely from the customer's cart."""
        if self.locked:
            return {"error": "This order is already placed. Call start_new_order first."}
        name = find_item(item_name)
        if name is None or name not in self.cart:
            return {"error": "That item is not in the cart.", "cart": self._bill()}
        del self.cart[name]
        self.pending = None
        return {"removed": name, "cart": self._bill()}

    def view_cart(self) -> dict:
        """Show what is in the cart right now, with prices and the total."""
        if not self.cart:
            return {"cart_is_empty": True}
        return {"cart": self._bill(), "order_placed": self.locked}

    def prepare_order(self, customer_name: str, phone: str, address: str) -> dict:
        """Check the customer's details and build the receipt. Call this only after you
        have the name, phone number and full address. Show the receipt to the customer
        and ask them to confirm with yes or no."""
        if self.locked:
            return {"error": "This order is already placed. Call start_new_order first."}
        if not self.cart:
            return {"error": "The cart is empty. Ask the customer what they would like to order."}
        name = (customer_name or "").strip()
        if len(name) < 2:
            return {"error": "Please ask the customer for their name."}
        cleaned_phone = clean_phone(phone)
        if cleaned_phone is None:
            return {"error": "Invalid phone number. Ask for a Pakistani mobile number "
                             "like 03001234567."}
        clean_address = (address or "").strip()
        if clean_address.lower() in ("", DELIVERY_AREA.lower()) or len(clean_address) < 5:
            return {"error": f"Ask for the exact address (house, street and area) in {DELIVERY_AREA}."}
        self.pending = {"name": name, "phone": cleaned_phone, "address": clean_address}
        return {"status": "ready_for_customer_confirmation", "customer": self.pending,
                "bill": self._bill(), "delivery_time": DELIVERY_TIME}

    def confirm_order(self) -> dict:
        """Place the order. Call this ONLY after the customer said yes to the receipt."""
        if self.locked:
            return {"error": "This order is already placed."}
        if not self.pending or not self.cart:
            return {"error": "Call prepare_order first and get the customer's confirmation."}
        self.locked = True
        return {"status": "order_placed",
                "order_id": datetime.now().strftime("%Y%m%d-%H%M%S"),
                "delivery_time": DELIVERY_TIME}

    def start_new_order(self) -> dict:
        """Clear everything and start a fresh order (use after an order was placed)."""
        self.cart = {}
        self.pending = None
        self.locked = False
        return {"status": "new_order_started"}
