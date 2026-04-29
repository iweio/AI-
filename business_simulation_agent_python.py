import random
from dataclasses import dataclass, field
from typing import List, Dict, Callable

# -----------------------------
# User / Customer Definition
# -----------------------------
@dataclass
class Customer:
    id: int
    budget: float
    preference: str
    sensitivity: float  # price sensitivity (0-1)
    loyalty: float = 0.0

    def decide(self, product_price: float, product_type: str) -> bool:
        """Simulate purchase decision"""
        price_factor = max(0, 1 - (product_price / self.budget) * self.sensitivity)
        preference_factor = 1 if product_type == self.preference else 0.5
        probability = price_factor * preference_factor * (1 + self.loyalty)
        return random.random() < probability


# -----------------------------
# Product Definition
# -----------------------------
@dataclass
class Product:
    name: str
    price: float
    category: str


# -----------------------------
# Strategy Definition
# -----------------------------
@dataclass
class Strategy:
    name: str
    pricing_fn: Callable[[float], float]

    def apply(self, base_price: float) -> float:
        return self.pricing_fn(base_price)


# -----------------------------
# Simulation Environment
# -----------------------------
@dataclass
class Simulation:
    customers: List[Customer]
    product: Product
    strategy: Strategy
    steps: int = 30
    revenue: float = 0.0
    history: List[Dict] = field(default_factory=list)

    def run(self):
        for step in range(self.steps):
            price = self.strategy.apply(self.product.price)
            purchases = 0

            for customer in self.customers:
                if customer.decide(price, self.product.category):
                    purchases += 1
                    self.revenue += price
                    customer.loyalty += 0.05
                else:
                    customer.loyalty *= 0.99

            self.history.append({
                "step": step,
                "price": price,
                "purchases": purchases,
                "revenue": self.revenue
            })

            print(f"Step {step}: price={price:.2f}, purchases={purchases}, revenue={self.revenue:.2f}")


# -----------------------------
# Example Strategies
# -----------------------------

def discount_strategy(base_price: float) -> float:
    return base_price * 0.8


def surge_pricing(base_price: float) -> float:
    return base_price * random.uniform(1.0, 1.5)


def static_price(base_price: float) -> float:
    return base_price


# -----------------------------
# Generate Customers
# -----------------------------

def generate_customers(n: int) -> List[Customer]:
    customers = []
    for i in range(n):
        customers.append(Customer(
            id=i,
            budget=random.uniform(50, 500),
            preference=random.choice(["tech", "fashion", "food"]),
            sensitivity=random.uniform(0.2, 1.0)
        ))
    return customers


# -----------------------------
# Run Simulation
# -----------------------------
if __name__ == "__main__":
    customers = generate_customers(100)

    product = Product(
        name="Smart Gadget",
        price=100,
        category="tech"
    )

    strategy = Strategy(
        name="Discount Strategy",
        pricing_fn=discount_strategy
    )

    sim = Simulation(
        customers=customers,
        product=product,
        strategy=strategy,
        steps=20
    )

    sim.run()

    # Final result
    print("\nFinal Revenue:", sim.revenue)
