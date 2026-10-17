# 📘 Cross-border & Student Finance Agent

An AI-powered student finance assistant that helps users track expenses, manage budgets, compare cross-border payment providers, and identify payment risks.

## How It Works

**Workflow:** Streamlit chat page → Claude (LLM) → 6 tools → Simulated data (`data.json`)

| Tier | Tools | Rule |
|---|---|---|
| 1. Read-only | `get_budget_status`, `compare_providers`, `check_payment_risk` | Reads information without changing data. |
| 2. Own data | `add_expense`, `set_budget` | Edits the user's own records. |
| 3. Payment | `simulate_payment` | Creates a pending request only. The user must press Confirm in the UI. Medium-risk payments also require a verification tick, checked in code. |

## Risk Levels

- **High risk:** Scam-like wording; the payment is blocked.
- **Medium risk:** Tuition or housing payment to a personal account, an unverified payee, or a payment of RM5,000 or more. Requires the verification tick.
- **Low risk:** Normal confirmation process.

Every action is recorded in `logs/actions.log` with a timestamp for execution evidence.

## Setup

### 1. Install Python

Install Python 3.10 or later.

### 2. Install Dependencies

Run this command in your terminal:

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

**Mac/Linux:**

```bash
export ANTHROPIC_API_KEY="your-key"
```

**Windows PowerShell:**

```powershell
$env:ANTHROPIC_API_KEY="your-key"
```

**Security:** Never commit your real API key to GitHub.

### 4. Run the Application

```bash
streamlit run app.py
```

## Run Tests

```bash
pytest -v
```

## Try These Examples

- `I spent RM15 on lunch`
- `Set my budget to RM1500`
- `Compare ways to send RM2000 to the UK`
- `Pay RM2000 tuition to Ahmad Tan (personal account) via Wise` — Medium risk; confirmation requires the verification tick.
- `Pay RM2000 tuition to University of Sample Tuition Office (business) via Wise` — Low risk; normal confirmation.
- `Pay RM100 urgent gift card to Sam via Wise` — Blocked due to scam-like wording.

## Known Limitations

- Exchange rates and fees are simulated.
- Risk checks use simple rules.
- The verification tick is self-declared.
- No income-tracking tool.
- No editing or deleting expenses.
- No per-month budget tracking.
- No real wallet or payment APIs.
