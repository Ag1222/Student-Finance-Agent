
import re
import streamlit as st

from tools import (
    add_expense,
    get_budget_status,
    compare_providers,
    check_payment_risk,
    simulate_payment,
)

st.set_page_config(
    page_title="Student Finance Agent",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Student Finance Agent")
st.caption("Your student finance assistant for everyday spending and overseas payments.")

st.info(
    "Demo only: provider fees and rates are illustrative. "
    "No real payments are made."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! 👋 I'm your Student Finance Agent.\n\n"
                "Try telling me about an expense, comparing transfer "
                "providers, or reviewing a simulated payment."
            ),
        }
    ]

if "pending_payment" not in st.session_state:
    st.session_state.pending_payment = None


# ---------- Budget sidebar ----------
with st.sidebar:
    st.header("📊 Your Budget")

    try:
        budget = get_budget_status()
        st.metric("Monthly budget", f"RM {budget['budget_myr']:.2f}")
        st.metric("Total spent", f"RM {budget['spent_myr']:.2f}")
        st.metric("Remaining", f"RM {budget['remaining_myr']:.2f}")

        progress = max(
            0.0,
            min(1.0, budget["used_percentage"] / 100),
        )
        st.progress(progress)
        st.caption(f"{budget['used_percentage']:.1f}% used")
        st.write(budget["warning"])

    except Exception as exc:
        st.error(f"Could not load budget: {exc}")

    st.divider()
    st.subheader("💬 Example messages")
    st.markdown(
        """
        - I spent RM15 on lunch
        - Compare ways to send RM2000 to the UK
        - Pay RM2000 tuition to Ahmad Tan (personal account) via Wise
        """
    )


# ---------- Process chat messages ----------
def process_message(message):
    text = message.strip()
    lower = text.lower()

    amount_match = re.search(
    r"\b(?:RM|MYR|USD|SGD|GBP|EUR)?\s*(\d+(?:\.\d{1,2})?)",
    text,
    re.IGNORECASE,
)
    amount = float(amount_match.group(1)) if amount_match else None

    # 1. Log an expense
    if "spent" in lower or "expense" in lower or "record expense" in lower:
        if amount is None:
            return "Please include the expense amount, e.g. `I spent RM15 on lunch`."


        currency_match = re.search(
            r"\b(RM|MYR|USD|SGD|GBP|EUR)\b",
            text,
            re.IGNORECASE,
        )
        currency = (
            currency_match.group(1).upper()
            if currency_match
            else "MYR"
        )
        if currency == "RM":
            currency = "MYR"

        description_match = re.search(
            r"\b(?:on|for)\s+(.+)$",
            text,
            re.IGNORECASE,
        )
        description = (
            description_match.group(1).strip(" .!?")
            if description_match
            else "General expense"
        )

        result = add_expense(amount, currency, description)

        if result.get("success"):
            budget = get_budget_status()
            return (
                f"✅ **Expense recorded!**\n\n"
                f"- Description: {description}\n"
                f"- Amount: {currency} {amount:.2f}\n\n"
                f"Your MYR budget now has **RM {budget['remaining_myr']:.2f} "
                f"remaining** ({budget['used_percentage']:.1f}% used).\n\n"
                f"_{budget['warning']}_"
            )

        return f"❌ {result.get('message', result)}"

    # 2. Compare transfer providers
    if any(word in lower for word in ["compare", "comparison"]):
        if amount is None:
            return "Please include an amount, e.g. `Compare ways to send RM2000 to the UK`."

        results = compare_providers(amount)

        if isinstance(results, dict):
            return f"Could not compare providers: {results}"

        lines = [
            f"### 💱 Provider comparison for RM {amount:.2f}",
            "",
            "| Provider | Sample fee | Estimated foreign currency received |",
            "|---|---:|---:|",
        ]

        for item in results:
            lines.append(
                f"| {item['provider']} "
                f"| RM {item['fee_myr']:.2f} "
                f"| {item['foreign_received']:.2f} |"
            )

        lines.append(
            "\n*These figures use sample rates and fees. "
            "They are not live quotes or verified GBP transfer estimates.*"
        )
        return "\n".join(lines)

    # 3. Review a simulated payment
    if lower.startswith("pay ") or lower.startswith("simulate payment"):
        if amount is None:
            return "Please include the payment amount."

        payee_match = re.search(
            r"\bto\s+(.+?)(?:\s+via\b|$)",
            text,
            re.IGNORECASE,
        )
        purpose_match = re.search(
    r"\bpay\s+(?:RM|MYR|USD|SGD|GBP|EUR)?\s*\d+(?:\.\d{1,2})?"
    r"\s+(.+?)\s+to\b",
    text,
    re.IGNORECASE,
)
        provider_match = re.search(
            r"\bvia\s+(.+)$",
            text,
            re.IGNORECASE,
        )

        if not payee_match:
            return (
                "Please specify the recipient, e.g. "
                "`Pay RM2000 tuition to University via Wise`."
            )

        payee = payee_match.group(1).strip(" .")
        purpose = (
            purpose_match.group(1).strip()
            if purpose_match
            else "General payment"
        )
        provider = (
            provider_match.group(1).strip(" .")
            if provider_match
            else "Not specified"
        )

        risk = check_payment_risk(payee, amount, purpose)

        st.session_state.pending_payment = {
            "payee": payee,
            "amount": amount,
            "purpose": purpose,
            "provider": provider,
            "risk": risk,
        }

        reasons = risk.get("reasons", [])
        if risk.get("risk") == "high":
            reason_text = "\n".join(f"- {reason}" for reason in reasons)
            return (
                f"⚠️ **Payment flagged for verification**\n\n"
                f"- Recipient: {payee}\n"
                f"- Amount: RM {amount:.2f}\n"
                f"- Purpose: {purpose}\n"
                f"- Provider: {provider}\n\n"
                f"**Reasons:**\n{reason_text}\n\n"
                "Review the payment below. A verification tick is required "
                "to attempt confirmation, but high-risk payments remain blocked."
            )

        return (
            f"🔎 **Payment review**\n\n"
            f"- Recipient: {payee}\n"
            f"- Amount: RM {amount:.2f}\n"
            f"- Purpose: {purpose}\n"
            f"- Provider: {provider}\n\n"
            "No basic risk rules were triggered. This does not guarantee safety. "
            "Review the details and verify the recipient before proceeding."
        )

    return (
        "I can help with three types of requests:\n\n"
        "1. **Record an expense:** `I spent RM15 on lunch`\n"
        "2. **Compare providers:** `Compare ways to send RM2000 to the UK`\n"
        "3. **Review a payment:** `Pay RM2000 tuition to Ahmad Tan "
        "(personal account) via Wise`"
    )


# ---------- Display conversation ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask about your expenses or payments...")

if user_message:
    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    try:
        response = process_message(user_message)
    except Exception as exc:
        response = f"Sorry, something went wrong: {exc}"

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.rerun()


# ---------- Payment verification and confirmation ----------
pending = st.session_state.pending_payment

if pending:
    st.divider()
    st.subheader("🔐 Payment verification")
    st.write(f"**Recipient:** {pending['payee']}")
    st.write(f"**Amount:** RM {pending['amount']:.2f}")
    st.write(f"**Purpose:** {pending['purpose']}")
    st.write(f"**Provider:** {pending['provider']}")

    high_risk = pending["risk"].get("risk") == "high"

    if high_risk:
        st.error(
            "High-risk payment. Confirmation cannot override the "
            "payment tool's risk-blocking rules."
        )

    verified = st.checkbox(
        "I have independently verified the recipient and payment details.",
        key="payment_verified",
    )

    if st.button(
        "Confirm simulated payment",
        disabled=not verified,
    ):
        result = simulate_payment(
            pending["payee"],
            pending["amount"],
            pending["purpose"],
            confirmed=True,
        )

        if result.get("status") == "simulated":
            st.success(result["message"])
        else:
            st.error(result.get("message", "Payment was not completed."))
            if result.get("risk_reasons"):
                for reason in result["risk_reasons"]:
                    st.write(f"- {reason}")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    f"**Payment result:** {result.get('status', 'unknown')}\n\n"
                    f"{result.get('message', 'No further details.')}"
                ),
            }
        )
        st.session_state.pending_payment = None
        st.session_state.pop("payment_verified", None)
        st.rerun()

    if st.button("Cancel payment"):
        st.session_state.pending_payment = None
        st.session_state.pop("payment_verified", None)
        st.rerun()
