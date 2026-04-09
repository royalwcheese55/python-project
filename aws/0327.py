from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int
    category: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Item name is required.")
        if self.price < 0:
            raise ValueError(f"Price cannot be negative for item '{self.name}'.")
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError(f"Quantity must be a positive integer for item '{self.name}'.")
        if not self.category:
            raise ValueError(f"Category is required for item '{self.name}'.")

    @property
    def total_price(self) -> float:
        return self.price * self.quantity


@dataclass
class Cart:
    items: List[CartItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.items is None:
            raise ValueError("Items list cannot be None.")
        for item in self.items:
            if not isinstance(item, CartItem):
                raise TypeError("All cart entries must be CartItem objects.")

    @property
    def subtotal(self) -> float:
        return sum(item.total_price for item in self.items)

    def get_items_by_category(self, category: str) -> List[CartItem]:
        return [item for item in self.items if item.category == category]

    def get_item_by_name(self, name: str) -> CartItem | None:
        for item in self.items:
            if item.name == name:
                return item
        return None


@dataclass
class DiscountResult:
    promotion: str
    amount: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "promotion": self.promotion,
            "amount": round(self.amount, 2)
        }


class Promotion(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def calculate_discount(self, cart: Cart) -> float:
        pass


@dataclass
class PercentageDiscount(Promotion):
    percent: float

    def __post_init__(self) -> None:
        if self.percent < 0:
            raise ValueError("Percentage discount cannot be negative.")

    @property
    def name(self) -> str:
        return f"{self.percent}% off cart"

    def calculate_discount(self, cart: Cart) -> float:
        return cart.subtotal * (self.percent / 100.0)


@dataclass
class CategoryDiscount(Promotion):
    category: str
    percent: float

    def __post_init__(self) -> None:
        if not self.category:
            raise ValueError("Category is required.")
        if self.percent < 0:
            raise ValueError("Category discount cannot be negative.")

    @property
    def name(self) -> str:
        return f"{self.percent}% off {self.category}"

    def calculate_discount(self, cart: Cart) -> float:
        category_total = sum(item.total_price for item in cart.get_items_by_category(self.category))
        return category_total * (self.percent / 100.0)


@dataclass
class BuyXGetYFree(Promotion):
    product_name: str
    buy_x: int
    get_y: int

    def __post_init__(self) -> None:
        if not self.product_name:
            raise ValueError("Product name is required.")
        if not isinstance(self.buy_x, int) or self.buy_x <= 0:
            raise ValueError("buy_x must be a positive integer.")
        if not isinstance(self.get_y, int) or self.get_y <= 0:
            raise ValueError("get_y must be a positive integer.")

    @property
    def name(self) -> str:
        return f"Buy {self.buy_x} get {self.get_y} free on {self.product_name}"

    def calculate_discount(self, cart: Cart) -> float:
        item = cart.get_item_by_name(self.product_name)
        if item is None:
            return 0.0

        group_size = self.buy_x + self.get_y
        free_units = (item.quantity // group_size) * self.get_y
        return free_units * item.price


class PricingEngine:
    def __init__(self, promotions: List[Promotion]) -> None:
        self.promotions = promotions or []

    def checkout(self, cart: Cart) -> Dict[str, Any]:
        subtotal = cart.subtotal
        discounts: List[DiscountResult] = []
        total_discount = 0.0

        for promotion in self.promotions:
            raw_discount = promotion.calculate_discount(cart)

            if raw_discount < 0:
                raise ValueError(f"Promotion '{promotion.name}' produced a negative discount.")

            remaining_amount = subtotal - total_discount
            applied_discount = min(raw_discount, remaining_amount)

            if applied_discount > 0:
                discounts.append(DiscountResult(promotion.name, applied_discount))
                total_discount += applied_discount

            if total_discount >= subtotal:
                total_discount = subtotal
                break

        final_total = max(0.0, subtotal - total_discount)

        return {
            "subtotal": round(subtotal, 2),
            "discounts": [d.to_dict() for d in discounts],
            "final_total": round(final_total, 2)
        }


def build_cart_from_dicts(raw_items: List[Dict[str, Any]]) -> Cart:
    required_fields = {"name", "price", "quantity", "category"}

    cart_items: List[CartItem] = []
    for idx, raw in enumerate(raw_items, start=1):
        missing = required_fields - raw.keys()
        if missing:
            raise ValueError(f"Item #{idx} is missing required fields: {sorted(missing)}")

        cart_items.append(
            CartItem(
                name=raw["name"],
                price=float(raw["price"]),
                quantity=raw["quantity"],
                category=raw["category"],
            )
        )

    return Cart(cart_items)


def main() -> None:
    raw_data = [
        {"name": "Keyboard", "price": 100, "quantity": 1, "category": "electronics"},
        {"name": "Mouse", "price": 50, "quantity": 2, "category": "electronics"},
        {"name": "Notebook", "price": 20, "quantity": 3, "category": "stationery"},
    ]

    cart = build_cart_from_dicts(raw_data)

    promotions = [
        PercentageDiscount(10),
        CategoryDiscount("electronics", 20),
        BuyXGetYFree("Notebook", 2, 1),
    ]

    engine = PricingEngine(promotions)
    result = engine.checkout(cart)
    print(result)


if __name__ == "__main__":
    main()