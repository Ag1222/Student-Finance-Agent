# Student Finance Agent

A student-focused finance assistant designed to help students manage expenses, monitor budgets, compare payment providers, identify potentially risky payments, and review simulated payments.

## Features

1. **Expense Tracking** — Record expenses in MYR or supported foreign currencies.
2. **Budget Monitoring** — View budget status and receive warnings when spending reaches 80% or 100% of the budget.
3. **Payment Provider Comparison** — Compare illustrative costs and estimated foreign-currency amounts for TNG eWallet, GrabPay, Wise, and bank transfers.
4. **Payment Risk Checks** — Apply simple rules to flag potentially suspicious or unusual payments.
5. **Payment Simulation** — Review and confirm a simulated payment without sending real money.

## Technology Stack

- Python
- Streamlit
- JSON for sample data storage
- pytest for automated testing

## Prerequisites

- Python 3.11 or newer
- Git
- pip

## Installation

Clone the repository:

```bash
git clone https://github.com/Ag1222/Student-Finance-Agent.git
cd Student-Finance-Agent
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Run the Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

The test suite checks expense validation, budget warnings, provider comparisons, payment-risk rules, and payment confirmation requirements.

## Deployment Instructions

The application can be deployed using Streamlit Community Cloud.

1. Push the source code to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Create a new app and select this repository.
4. Select the appropriate branch and `app.py` as the main file.
5. Deploy the application and test the public URL.

For local execution, follow the installation and run instructions above.

## Important Limitations

- Provider fees and exchange rates are illustrative sample values, not live financial quotes.
- Budget monitoring currently counts MYR expenses; supported foreign-currency expenses are automatically converted into MYR.
- Payment-risk checks use simple rules and do not guarantee fraud detection.
- Payments are simulated only. The application does not transfer real money.
- The application is a prototype for educational and demonstration purposes, not professional financial advice.

## Repository Structure

```text
Student-Finance-Agent/
├── app.py
├── tools.py
├── data.json
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_tools.py
```

## GitHub Repository

https://github.com/Ag1222/Student-Finance-Agent
