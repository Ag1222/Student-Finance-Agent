
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
st.write(
    "A demo assistant for managing student expenses, "
    "comparing payment providers, and checking payment risks."
)

st.info(
    "Demo mode: This app uses sample data and simulated payments. "
    "It does not send real money or use live exchange rates."
)


def show_result(result):
    """Display a tool's result."""
    if isinstance(result, (dict, list)):
        st.json(result)
    else:
        st.write(result)


# Create five sections for the five finance tools.
expense_tab, budget_tab, compare_tab, risk_tab, payment_tab = st.tabs(
    [
        "1. Add Expense",
        "2. Budget Status",
        "3. Compare Providers",
        "4. Check Payment Risk",
        "5. Simulate Payment",
    ]
)


# TOOL 1: Add an expense
with expense_tab:
    st.subheader("Record a new expense")

    with st.form("expense_form"):
        amount = st.number_input(
            "Amount",
            min_value=0.01,
            value=50.0,
            step=1.0,
        )
        currency = st.selectbox(
            "Currency",
            ["MYR", "USD", "SGD", "GBP", "EUR"],
        )
        description = st.text_input(
            "Description",
            placeholder="e.g. Lunch",
        )
        expense_submitted = st.form_submit_button("Add Expense")

    if expense_submitted:
        try:
            result = add_expense(amount, currency, description)
            st.success("Expense tool executed.")
            show_result(result)
        except Exception as exc:
            st.error(f"Could not add expense: {exc}")


# TOOL 2: Check the budget
with budget_tab:
    st.subheader("Check your monthly budget")
    st.write("View your remaining budget and spending warnings.")

    if st.button("Check Budget", key="check_budget"):
        try:
            result = get_budget_status()
            show_result(result)
        except Exception as exc:
            st.error(f"Could not check budget: {exc}")


# TOOL 3: Compare payment providers
with compare_tab:
    st.subheader("Compare overseas payment providers")

    compare_amount = st.number_input(
        "Amount to send (MYR)",
        min_value=1.0,
        value=2000.0,
        step=100.0,
        key="compare_amount",
    )

    if st.button("Compare Providers"):
        try:
            result = compare_providers(compare_amount)
            show_result(result)
            st.caption(
                "Provider fees and exchange rates are illustrative "
                "sample values, not live quotes."
            )
        except Exception as exc:
            st.error(f"Could not compare providers: {exc}")


# TOOL 4: Check payment risk
with risk_tab:
    st.subheader("Check whether a payment looks risky")

    with st.form("risk_form"):
        risk_payee = st.text_input(
            "Recipient",
            placeholder="e.g. University or personal account",
        )
        risk_amount = st.number_input(
            "Payment amount (MYR)",
            min_value=0.01,
            value=2000.0,
            step=100.0,
            key="risk_amount",
        )
        risk_purpose = st.text_input(
            "Purpose",
            placeholder="e.g. Tuition fees",
        )
        risk_submitted = st.form_submit_button("Check Risk")

    if risk_submitted:
        try:
            result = check_payment_risk(
                risk_payee,
                risk_amount,
                risk_purpose,
            )
            show_result(result)
            st.caption(
                "This is a basic rule-based demonstration, "
                "not a guarantee that a payment is safe."
            )
        except Exception as exc:
            st.error(f"Could not check payment risk: {exc}")


# TOOL 5: Simulate a payment with explicit confirmation
with payment_tab:
    st.subheader("Simulate a payment")
    st.warning(
        "No real payment will be made. Risky payments should be blocked."
    )

    with st.form("payment_form"):
        payee = st.text_input(
            "Recipient",
            placeholder="e.g. University",
        )
        payment_amount = st.number_input(
            "Payment amount (MYR)",
            min_value=0.01,
            value=2000.0,
            step=100.0,
            key="payment_amount",
        )
        purpose = st.text_input(
            "Purpose",
            placeholder="e.g. Tuition fees",
        )
        payment_submitted = st.form_submit_button(
            "Review Payment"
        )

    if payment_submitted:
        try:
            risk_result = check_payment_risk(
                payee,
                payment_amount,
                purpose,
            )

            # Save the proposed payment until the user decides.
            st.session_state["pending_payment"] = {
                "payee": payee,
                "amount_myr": payment_amount,
                "purpose": purpose,
                "risk_result": risk_result,
            }
        except Exception as exc:
            st.error(f"Could not review payment: {exc}")

    pending = st.session_state.get("pending_payment")

    if pending:
        st.markdown("---")
        st.subheader("Review before confirmation")
        st.write(f"**Recipient:** {pending['payee']}")
        st.write(f"**Amount:** RM {pending['amount_myr']:.2f}")
        st.write(f"**Purpose:** {pending['purpose']}")
        st.write("**Risk-check result:**")
        show_result(pending["risk_result"])

        st.warning(
            "Read the risk result before proceeding. "
            "The payment tool performs its own risk checks."
        )

        if st.button("Confirm Simulated Payment"):
            try:
                result = simulate_payment(
                    pending["payee"],
                    pending["amount_myr"],
                    pending["purpose"],
                    confirmed=True,
                )
                show_result(result)
            except Exception as exc:
                st.error(f"Payment simulation failed: {exc}")
            finally:
                st.session_state.pop("pending_payment", None)

        if st.button("Cancel Payment"):
            st.session_state.pop("pending_payment", None)
            st.info("Proposed payment cancelled.")
