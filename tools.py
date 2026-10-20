
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")

SUPPORTED_CURRENCIES = {
    "MYR", "USD", "SGD", "GBP", "EUR", "IDR", "CNY"
}


def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)



def add_expense(amount, currency, description):
    """Record an expense in MYR or a supported foreign currency."""
    currency = currency.upper()

    if currency not in SUPPORTED_CURRENCIES:
        return {"success": False, "message": "Unsupported currency."}

    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return {"success": False, "message": "Amount must be positive."}

    if not description.strip():
        return {"success": False, "message": "Description is required."}

    data = load_data()

    # Store the original expense amount and currency.
    data.setdefault("expenses", []).append({
        "amount": round(amount, 2),
        "currency": currency,
        "description": description.strip()
    })

    save_data(data)

    return {"success": True, "message": "Expense recorded."}



def get_budget_status():
    """Calculate all expenses in MYR and show remaining budget."""
    data = load_data()
    budget = data["budget_myr"]

    # Rates represent foreign currency units per 1 MYR.
    rates = {}
    providers = data.get("providers", {})

    if isinstance(providers, dict):
        provider_list = providers.values()
    else:
        provider_list = providers

    for provider in provider_list:
        if not isinstance(provider, dict):
            continue

        provider_rates = provider.get("rates", {})
        for curr, rate in provider_rates.items():
            if isinstance(rate, (int, float)) and rate > 0:
                rates.setdefault(curr.upper(), rate)

    rates["MYR"] = 1.0
    spent = 0.0

    for expense in data.get("expenses", []):
        currency = expense["currency"].upper()
        amount = expense["amount"]

        if currency == "MYR":
            amount_myr = amount
        elif currency in rates:
            amount_myr = amount / rates[currency]
        else:
            raise ValueError(
                f"Missing exchange rate for {currency}. "
                "Please add its rate to data.json."
            )

        spent += amount_myr

    remaining = budget - spent
    percentage = spent / budget * 100 if budget > 0 else 0

    if spent >= budget:
        warning = "Budget reached or exceeded!"
    elif percentage >= 80:
        warning = "Warning: 80% or more of your budget is used."
    else:
        warning = "Budget is within limits."

    return {
        "budget_myr": budget,
        "spent_myr": round(spent, 2),
        "remaining_myr": round(remaining, 2),
        "used_percentage": round(percentage, 2),
        "warning": warning
    }


def compare_providers(amount, target_currency="SGD", source_currency="MYR"):
    """Compare transfer providers using sample exchange rates."""
    if (
        not isinstance(amount, (int, float))
        or isinstance(amount, bool)
        or amount <= 0
    ):
        return {"error": "Transfer amount must be positive."}

    source_currency = source_currency.upper()
    target_currency = target_currency.upper()

    if (
        source_currency not in SUPPORTED_CURRENCIES
        or target_currency not in SUPPORTED_CURRENCIES
    ):
        return {"error": "Unsupported source or destination currency."}

    data = load_data()
    providers = data.get("providers", {})
    results = []

    # Support providers stored as either a dictionary or a list.
    if isinstance(providers, dict):
        provider_items = providers.items()
    else:
        provider_items = [
            (provider.get("name", f"Provider {i + 1}"), provider)
            for i, provider in enumerate(providers)
            if isinstance(provider, dict)
        ]

    for name, provider in provider_items:
        if not isinstance(provider, dict):
            continue

        fee = provider.get("fee_myr")
        rates = provider.get("rates", {})

        if not isinstance(rates, dict):
            continue

        # Rates mean foreign currency units received for 1 MYR.
        source_rate = (
            1.0 if source_currency == "MYR"
            else rates.get(source_currency)
        )
        target_rate = (
            1.0 if target_currency == "MYR"
            else rates.get(target_currency)
        )

        # Skip this provider if its data is incomplete or invalid.
        if (
            not isinstance(fee, (int, float))
            or isinstance(fee, bool)
            or fee < 0
            or not isinstance(source_rate, (int, float))
            or isinstance(source_rate, bool)
            or source_rate <= 0
            or not isinstance(target_rate, (int, float))
            or isinstance(target_rate, bool)
            or target_rate <= 0
        ):
            continue

        # Convert the MYR fee into the source currency.
        fee_in_source = fee * source_rate

        # Convert source currency to MYR, subtract the fee,
        # then convert the remainder to the destination currency.
        remaining_source = max(0, amount - fee_in_source)
        received = (remaining_source / source_rate) * target_rate

        results.append({
            "provider": name,
            "fee_myr": round(fee, 2),
            "exchange_rate": round(target_rate / source_rate, 6),
            "currency": target_currency,
            "foreign_received": round(received, 2),
            "effective_cost_myr": round(fee, 2),
        })

    if not results:
        return {
            "error": (
                f"No providers have valid sample rates for "
                f"{source_currency} to {target_currency}. "
                "Check the rates in data.json."
            )
        }

    return sorted(
        results,
        key=lambda item: item["foreign_received"],
        reverse=True,
    )

def check_payment_risk(payee, amount_myr, purpose):
    """Apply simple rules to flag potentially risky payments."""
    reasons = []

    if not payee.strip():
        reasons.append("Payee name is missing.")

    if not isinstance(amount_myr, (int, float)) or isinstance(amount_myr, bool) or amount_myr <= 0:
        reasons.append("Payment amount must be positive.")
    elif amount_myr >= 5000:
        reasons.append("Large payment requires extra checking.")

    suspicious_words = {"personal", "unknown", "unverified"}
    if any(word in payee.lower() for word in suspicious_words):
        reasons.append("Payee name matches a basic risk rule.")

    if "tuition" in purpose.lower() and "personal" in payee.lower():
        reasons.append("Tuition payment to a personal account needs verification.")

    return {
        "risk": "high" if reasons else "low",
        "reasons": reasons,
        "message": (
            "Payment flagged. Do not proceed until reviewed."
            if reasons else
            "No basic risk rules triggered. This does not guarantee safety."
        )
    }


def simulate_payment(payee, amount_myr, purpose, confirmed=False):
    """Simulate a payment only after explicit confirmation."""
    if not isinstance(amount_myr, (int, float)) or isinstance(amount_myr, bool) or amount_myr <= 0:
        return {"status": "refused", "message": "Amount must be positive."}

    if not payee.strip() or not purpose.strip():
        return {"status": "refused", "message": "Payee and purpose are required."}

    risk = check_payment_risk(payee, amount_myr, purpose)

    if risk["risk"] == "high":
        return {
            "status": "blocked",
            "message": risk["message"],
            "risk_reasons": risk["reasons"]
        }

    if confirmed is not True:
        return {
            "status": "awaiting_confirmation",
            "message": "Review the payment details and confirm before simulating."
        }

    return {
        "status": "simulated",
        "message": "Simulated payment completed. No real money was transferred.",
        "payee": payee,
        "amount_myr": round(amount_myr, 2),
        "purpose": purpose
    }

def set_budget(amount):
    """Set the user's monthly budget in MYR."""
    if (
        not isinstance(amount, (int, float))
        or isinstance(amount, bool)
        or amount <= 0
    ):
        return {"error": "Budget must be a positive amount."}

    data = load_data()
    data["budget_myr"] = round(float(amount), 2)
    save_data(data)

    return {
        "message": f"Monthly budget set to RM{amount:,.2f}.",
        "budget_myr": round(float(amount), 2),
    }
