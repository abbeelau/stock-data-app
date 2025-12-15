# 📈 Stock Data Fetcher

A beautiful web application to fetch and display real-time stock market data using Yahoo Finance API.

## Features

- 📊 Real-time stock prices and company information
- 📈 Interactive candlestick charts
- 📉 Historical data visualization
- 📥 Download data as CSV
- 🎨 Clean and intuitive interface

## Installation

1. Clone this repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Usage

Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
2. Select a time period for historical data
3. Click "Fetch Data"
4. View real-time data, charts, and company information
5. Download data as CSV if needed

## Example Tickers

- **AAPL** - Apple Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **TSLA** - Tesla Inc.
- **AMZN** - Amazon.com Inc.

## Data Source

This app uses the `yfinance` library to fetch data from Yahoo Finance. Data is delayed by approximately 15 minutes.

## Disclaimer

This app is for educational and informational purposes only. It is not intended for actual trading decisions.

## License

MIT License - Feel free to use and modify!
```

---

## File 4: `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*.pyc
*.pyo
*.pyd
.Python

# Virtual environments
venv/
env/
ENV/

# Streamlit
.streamlit/

# Data files
*.csv
*.txt
!requirements.txt

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
