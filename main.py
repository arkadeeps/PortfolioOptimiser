import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from scipy.optimize import minimize
import yfinance as yf
import time

# FUNCTIONS
##############################################################################

def get_date(input_string):  # gets date from user
    try:
        date = pd.to_datetime(input(input_string))
        return date
    except ValueError:
        print('Invalid date format, please try again')
        print('\n')
        return get_date(input_string)


def ticker_check(ticker):  # validates ticker using yfinance
    try:
        test = yf.Ticker(ticker).info
        if "regularMarketPrice" in test and test["regularMarketPrice"] is not None:
            print('\nTicker validated and stock added\n')
            return ticker
        else:
            raise ValueError
    except Exception:
        print('Invalid ticker, please try again\n')
        return ticker_check(input('Enter the next ticker you would like to add: ').upper())


def date_check():
    global end, start
    if end < start:
        print('End date cannot be less than start date.')
        end = get_date('Please enter valid end date (YYYY-MM-DD): ')
        date_check()


def ask_user_loop():
    global stock_tickers, add_more_stocks
    if add_more_stocks == 'y':
        new_stock = input('Enter the next ticker you would like to add: ').upper()
        if new_stock in stock_tickers:
            print('Duplicate stock, please enter a unique ticker\n')
        else:
            stock_tickers.append(ticker_check(new_stock))
        add_more_stocks = input('Would you like to add more stocks? y/n ').lower()
        ask_user_loop()
    elif add_more_stocks == 'n':
        stock_tickers = list(filter(None, stock_tickers))
        print("Your portfolio tickers:", stock_tickers, "\n")
        confirm = input('Does this look correct? y/n ').lower()
        if confirm != 'y':
            add_more_stocks = 'y'
            ask_user_loop()
    else:
        add_more_stocks = input('Invalid input, add more stocks? y/n ').lower()
        ask_user_loop()


def get_return_volatility_SR(weights):
    weights = np.array(weights)
    port_return = np.sum(log_ret.mean() * weights * 252)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 252, weights)))
    sharpe_ratio = port_return / port_volatility
    return np.array([port_return, port_volatility, sharpe_ratio])


def negative_sharpe(weights):
    return -get_return_volatility_SR(weights)[2]


def check_weight_sum(weights):
    return np.sum(weights) - 1


def minimize_volatility(weights):
    return get_return_volatility_SR(weights)[1]

##############################################################################

print('\nWelcome to Portfolio Optimizer\n')

# Get dates
start = get_date('Enter start date (YYYY-MM-DD): ')
end = get_date('Enter end date (YYYY-MM-DD): ')
date_check()

# Get tickers
stock_tickers = [ticker_check(input('Enter the first ticker: ').upper())]
stock_tickers.append(ticker_check(input('Enter the second ticker: ').upper()))
add_more_stocks = input('Would you like to add more stocks? y/n ').lower()
ask_user_loop()

# Download stock data
print(f'\nFetching portfolio data from {start.date()} to {end.date()}...\n')
stock_df = yf.download(stock_tickers, start=start, end=end, auto_adjust=True)["Close"]

# Benchmark (SP500 via SPY ETF)
# Benchmark (SP500 via SPY ETF)
spy = yf.download("SPY", start=start, end=end, auto_adjust=True)[["Close"]]
spy["TOTAL"] = (spy["Close"] / spy["Close"].iloc[0]) * 1000

print(stock_df.head(), "\n", stock_df.tail(), "\nData obtained successfully\n")
time.sleep(1)

# Calculate log returns
log_ret = np.log(stock_df / stock_df.shift(1))

# Optimization setup
constraints = ({'type': 'eq', 'fun': check_weight_sum})
bounds = tuple((0, 1) for _ in stock_tickers)
init_guess = [1/len(stock_tickers)] * len(stock_tickers)

print('Optimizing portfolio...\n')
optimized_results = minimize(negative_sharpe, init_guess,
                             method='SLSQP', bounds=bounds, constraints=constraints)
sharpe_ratio_result = -optimized_results.fun
weights_results_dict = dict(zip(stock_df.columns, optimized_results.x))

print(f"Optimal Sharpe Ratio: {sharpe_ratio_result:.4f}\n")
print("Optimized portfolio weights:\n")
for key, value in weights_results_dict.items():
    print(f"{key} : {value:.2%}")
print("")

# Portfolio growth
opt_return_df = pd.DataFrame()
for ticker, weight in weights_results_dict.items():
    opt_return_df[f"{ticker} allocated"] = (stock_df[ticker] / stock_df[ticker].iloc[0]) * weight * 1000
opt_return_df["TOTAL"] = opt_return_df.sum(axis=1)
opt_return_df["TOTAL 3Mo SMA"] = opt_return_df["TOTAL"].rolling(62).mean()

equal_weight_return_df = pd.DataFrame()
for ticker, weight in zip(stock_df.columns, init_guess):
    equal_weight_return_df[f"{ticker} allocated"] = (stock_df[ticker] / stock_df[ticker].iloc[0]) * weight * 1000
equal_weight_return_df["TOTAL"] = equal_weight_return_df.sum(axis=1)

# Plot portfolio vs benchmark
fig, ax = plt.subplots(figsize=(16, 9))
ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y, _: format(int(y), ',')))

spy["TOTAL"].plot(label="S&P500", lw=2, ls='-', c='y')
opt_return_df["TOTAL"].plot(label="Optimized", lw=2, c='g')
opt_return_df["TOTAL 3Mo SMA"].plot(label="Optimized 3M SMA", lw=2, ls='--', c='r')
equal_weight_return_df["TOTAL"].plot(label="Equal allocation", lw=2)

plt.ylabel("Portfolio Value ($)", fontsize=15)
plt.xlabel("Time", fontsize=15)
plt.title(f"Hypothetical growth of $1000 with {len(stock_tickers)} stocks", fontsize=24)
plt.legend()
plt.show()

# Efficient Frontier
frontier_y_axis = np.linspace(0, 0.3, 200)
frontier_x_axis = []

for possible_return in frontier_y_axis:
    vol_constraints = (
        {'type': 'eq', 'fun': check_weight_sum},
        {'type': 'eq', 'fun': lambda w: get_return_volatility_SR(w)[0] - possible_return}
    )
    result = minimize(minimize_volatility, init_guess, method='SLSQP', bounds=bounds, constraints=vol_constraints)
    frontier_x_axis.append(result['fun'])

fig2, ax2 = plt.subplots(figsize=(16, 9))
ax2.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
ax2.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))

ax2.plot(frontier_x_axis, frontier_y_axis, 'g--', lw=2.5, label='Efficient frontier')

scatter_x, scatter_y = get_return_volatility_SR(optimized_results.x)[1], get_return_volatility_SR(optimized_results.x)[0]
plt.scatter(scatter_x, scatter_y, s=200, c='green', edgecolors='black', alpha=.5, label="Optimal Sharpe Ratio")
plt.annotate(f"Sharpe: {sharpe_ratio_result:.4f}", xy=(scatter_x, scatter_y),
             xytext=(scatter_x+0.01, scatter_y), arrowprops=dict(facecolor='black', arrowstyle="->"))

plt.title("Efficient Frontier", fontsize=24)
plt.xlabel("Volatility", fontsize=15)
plt.ylabel("Return", fontsize=15)
plt.legend()
plt.show()
print("Thank you for using Portfolio Optimizer!")

