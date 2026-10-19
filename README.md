# 💰 Student Finance Agent

A Streamlit-based finance assistant designed to help students manage everyday expenses, monitor budgets, compare cross-border money transfers, and simulate payments.

> **Demo project:** Provider fees and exchange rates are illustrative sample values, not live financial quotes. No real payments are made.

## ✨ Features

### 1. Expense Tracking
- Record expenses through natural-language messages.
- Identify the expense amount and currency.
- Store expense records for budget monitoring.

### 2. Budget Monitoring
- View your monthly budget.
- Track total spending and remaining budget.
- Monitor budget usage and receive spending warnings.

### 3. Cross-Border Transfer Comparison
Compare estimated payouts across four sample providers:
- TNG eWallet
- GrabPay
- Wise
- Bank Transfer

Supported currencies:
| Currency | Code |
|---|---|
| Malaysian Ringgit | MYR |
| Singapore Dollar | SGD |
| Chinese Yuan | CNY |
| Indonesian Rupiah | IDR |
| US Dollar | USD |
| British Pound | GBP |
| Euro | EUR |

The comparison supports transfers between MYR and supported foreign currencies, including:
- Malaysia → Singapore
- Malaysia → China
- Malaysia → Indonesia
- Singapore → Malaysia
- China → Malaysia
- Indonesia → Malaysia

The app estimates the amount received after applying sample transfer fees and exchange rates, then ranks providers by estimated payout.

### 4. Payment Risk Checking
- Check payment details for potential risks.
- Review payment information before proceeding with a simulation.

### 5. Payment Simulation
- Simulate a payment using the available payment workflow.
- Review the simulated payment result.
- No real funds are transferred.

## 🛠️ Technology Stack

- **Python** — application logic and calculations
- **Streamlit** — interactive web interface
- **JSON** — local storage for sample financial data
- **pytest** — automated testing

## 📁 Project Structure

```text
Student-Finance-Agent/
├── app.py
├── tools.py
├── data.json
├── tests/
│   └── test_tools.py
├── README.md
└── requirements.txt
```

*Your local folder may contain additional development or backup files.*

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or later
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Student-Finance-Agent
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

If you have already downloaded the project, open its project folder in VS Code instead.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If your project contains `requirements.txt`, run:

```powershell
python -m pip install -r requirements.txt
```

If dependencies are not listed there yet, install the packages required by the project:

```powershell
python -m pip install streamlit pytest
```

### 4. Run the application

Run the following command from the folder containing `app.py`:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## 🧪 Running Tests

Run the automated tests from the project root:

```powershell
python -m pytest
```

The tests cover the finance tools and their expected behaviour. Run them after making code changes to check for regressions.

## 💬 Example Messages

Try entering these messages in the app:

```text
I spent RM15 on lunch
```

```text
Compare ways to send RM2000 to Singapore
```

```text
Compare ways to send RM2000 to China
```

```text
Compare ways to send RM2000 to Indonesia
```

```text
Compare ways to send SGD 2000 to Malaysia
```

```text
Compare ways to send CNY 3000 to Malaysia
```

```text
Compare ways to send IDR 20000000 to Malaysia
```

Use the payment simulation workflow to test a payment scenario supported by the app.

## ⚠️ Limitations

- Exchange rates and provider fees are illustrative sample data.
- Provider comparisons are estimates and may not reflect actual transfer costs or payouts.
- The app does not connect to live banking or payment services.
- Payment simulation does not transfer real money.
- Data is stored locally in JSON, so it is intended as a demonstration rather than a production financial application.

## 🔮 Future Improvements

- Integrate live exchange-rate APIs.
- Retrieve current provider fees and transfer limits.
- Add more currencies and destination countries.
- Improve transaction history and data persistence.
- Add stronger payment-risk checks and input validation.
- Introduce secure user accounts and persistent database storage.

## 📄 License

Add a license if you intend to distribute or open-source this project.
