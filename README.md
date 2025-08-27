# 📊 Portfolio Optimizer – Modern Portfolio Theory in Python  

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://www.python.org/)  
[![Pandas](https://img.shields.io/badge/Pandas-2.2.0-150458?style=flat-square&logo=pandas)](https://pandas.pydata.org/)  
[![NumPy](https://img.shields.io/badge/NumPy-2.0-013243?style=flat-square&logo=numpy)](https://numpy.org/)  
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9.0-3776AB?style=flat-square&logo=plotly)](https://matplotlib.org/)  
[![SciPy](https://img.shields.io/badge/SciPy-1.12-8CAAE6?style=flat-square&logo=scipy)](https://scipy.org/)  
[![yFinance](https://img.shields.io/badge/yFinance-Live_Data-green?style=flat-square&logo=yahoo)](https://pypi.org/project/yfinance/)  

A Python-based **Portfolio Optimizer** implementing **Modern Portfolio Theory (MPT)** to help investors design optimal portfolios.  
It fetches real-time stock data, calculates returns, risks, and Sharpe Ratios, and generates the **Efficient Frontier** to guide investment decisions.  

---

## ✨ Features  

- 📈 **Portfolio Construction** – Add multiple tickers interactively with validation  
- 🧮 **Sharpe Ratio Optimization** – Maximize returns per unit risk with SciPy’s optimization  
- 🏦 **Benchmarking** – Compare portfolio growth vs. **S&P 500 (SPY ETF)**  
- 📊 **Data Visualization** – Growth curves, rolling SMA, risk-return scatter plots, efficient frontier  
- 🔄 **Interactive CLI** – User-friendly prompts for tickers, dates, and portfolio adjustments  

---

## 🛠️ Tech Stack  

- **Language:** Python 3.11  
- **Data Analysis:** Pandas, NumPy  
- **Optimization:** SciPy (`minimize` for Sharpe Ratio / volatility)  
- **Visualization:** Matplotlib (growth curves, efficient frontier)  
- **Financial Data:** yFinance API (Yahoo Finance live data)  

---

## 📂 Project Structure  

```
portfolio-optimizer/
│── portfolio_optimizer.py    # Main script
│── requirements.txt          # Dependencies
│── README.md                 # Project documentation
```

---

## 🚀 Getting Started  

### 1️⃣ Clone the repository  

```bash
git clone https://github.com/yourusername/portfolio-optimizer.git
cd portfolio-optimizer
```

### 2️⃣ Install dependencies  

```bash
pip install -r requirements.txt
```

Or install manually:  

```bash
pip install pandas numpy matplotlib scipy yfinance
```

### 3️⃣ Run the optimizer  

```bash
python portfolio_optimizer.py
```

---

## ⚙️ How It Works  

1. **User Input** – Enter start date, end date, and stock tickers interactively  
2. **Data Fetching** – Download historical price data from Yahoo Finance (via `yFinance`)  
3. **Portfolio Construction** – Build equal-weight and optimized portfolios  
4. **Optimization** – Maximize Sharpe Ratio & calculate Efficient Frontier using `scipy.optimize`  
5. **Visualization** – Plot portfolio performance vs. S&P500 benchmark + Efficient Frontier  

---

## 📊 Example Outputs  

### Portfolio Growth vs S&P500  

- Optimized Portfolio  
- Equal Weighted Portfolio  
- Benchmark (S&P500 via SPY)  
- 3-Month Rolling SMA  

### Efficient Frontier  

- Curve showing return-volatility tradeoff  
- Highlighted point for **optimal Sharpe ratio portfolio**  

---

## 🔐 Key Concepts Implemented  

- **Log Returns** instead of arithmetic returns  
- **Modern Portfolio Theory (MPT)**  
- **Efficient Frontier Calculation**  
- **Sharpe Ratio Maximization**  
- **Rolling Averages (3M SMA)**  

---

## 📈 Future Improvements  

- Monte Carlo simulation for portfolio optimization  
- Support for alternative risk metrics (e.g., CVaR, Sortino Ratio)  
- Web-based dashboard using **Streamlit**  

---

## 🤝 Contributing  

Contributions are welcome!  

1. Fork the repo  
2. Create a new branch (`feature/your-feature`)  
3. Commit your changes  
4. Push and create a PR  

---

## 📝 License  

This project is licensed under the **MIT License** – feel free to use and modify.  

---

💡 *Built with Python, Finance, and Data Science love!*  
