
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")

SUPPORTED_CURRENCIES = {"MYR", "USD", "SGD", "GBP", "EUR"}


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
    data.setdefault("expenses", []).append({
        "amount": round(amount, 2),
        "currency": currency,
        "description": description.strip()
    })
    save_data(data)

    return {"success": True, "message": "Expense recorded."}


def get_budget_status():
    """Show remaining budget and warn at 80% and 100%."""
    data = load_data()
    budget = data["budget_myr"]

    # Only MYR expenses are counted until currency conversion is implemented.
    spent = sum(
        expense["amount"]
        for expense in data.get("expenses", [])
        if expense["currency"] == "MYR"
    )

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


def compare_providers(amount_myr):
    """Compare simulated fees and exchange rates for a MYR transfer."""
    if not isinstance(amount_myr, (int, float)) or isinstance(amount_myr, bool) or amount_myr <= 0:
        return {"error": "Transfer amount must be positive."}

    data = load_data()
    results = []

    for name, provider in data["providers"].items():
        fee = provider["fee_myr"]
        rate = provider["rate"]

        # rate means foreign currency received per MYR.
        foreign_received = max(0, amount_myr - fee) * rate
        results.append({
            "provider": name,
            "fee_myr": fee,
            "foreign_received": round(foreign_received, 2),
            "effective_cost_myr": round(fee, 2)
        })

    return sorted(results, key=lambda item: item["foreign_received"], reverse=True)


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
