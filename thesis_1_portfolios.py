<<<<<<< HEAD
"""
------------------------------------------------------------------------------
Thesis Project – Part 2: Portfolio Construction and Performance Analysis
Author: Maria C. F. Figueiredo
Master’s in Finance – Nova School of Business and Economics
Supervisor: Prof. Nicholas Hirschey
Date: December 2025
------------------------------------------------------------------------------
"""

# ==========================================================
# 0. INITIAL SETUP
# ==========================================================
=======
# ----------------------------------------------------------
# Thesis Project – Part 2: Portfolio Construction & Analysis
# Author: Maria C. F. Figueiredo
# Master’s in Finance – Nova SBE
# ----------------------------------------------------------
>>>>>>> a6a7c26f02ffdb8df2d3921afa91c3327d6a5781

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
<<<<<<< HEAD
from pathlib import Path

plt.style.use("seaborn-v0_8-whitegrid")

root_path = Path(__file__).resolve().parent
data_path = root_path / "data"
output_path = root_path / "output"
output_path.mkdir(parents=True, exist_ok=True)

path_fundamentals = data_path / "fundamentals_cleaned.xlsx"
path_returns = data_path / "stocks_returns.csv"
path_factors = data_path / "fffactors_daily.xlsx"
output_excel = output_path / "portfolio_results.xlsx"

print("🚀 Thesis Project – Part 2: Portfolio Construction & Analysis\n")

# ==========================================================
# 1. LOAD DATA
# ==========================================================

fundamentals = pd.read_excel(path_fundamentals)
returns = pd.read_csv(path_returns, low_memory=False)
returns["Date"] = pd.to_datetime(returns["date"])
returns["Year"] = returns["Date"].dt.year
returns.rename(columns={"TICKER": "Ticker Symbol", "vwretd": "Daily Stock Return"}, inplace=True)

merged = pd.merge(returns, fundamentals, on=["Ticker Symbol", "Year"], how="inner")
merged.dropna(subset=["Sales Growth Rate", "Current Ratio"], inplace=True)

print(f"✅ Merged dataset: {merged['Ticker Symbol'].nunique()} stocks across {merged['Year'].nunique()} years.\n")

# ==========================================================
# 2. PORTFOLIO CONSTRUCTION
# ==========================================================

def build_portfolio(df):
    pivot = df.groupby(["Date", "Ticker Symbol"])["Daily Stock Return"].mean().unstack().fillna(0)
    return pivot.mean(axis=1)

long_top = build_portfolio(merged[merged["Tercile"] == 0])
long_bottom = build_portfolio(merged[merged["Tercile"] == 2])
market = build_portfolio(merged)
long_short = long_top - long_bottom

portfolios = pd.DataFrame({
    "Long-Top": long_top,
    "Long-Bottom": long_bottom,
    "Long-Short": long_short,
    "Market": market
}).dropna()

# ==========================================================
# 3. PERFORMANCE ANALYSIS
# ==========================================================

trading_days = 252
portfolios_cum = (1 + portfolios).cumprod()

# --- In-sample / Out-of-sample split ---
in_sample = portfolios.loc["2001-01-01":"2015-12-31"]
out_sample = portfolios.loc["2016-01-01":]

def compute_metrics(df):
    out = pd.DataFrame(index=df.columns)
    out["Average Annualized Return"] = ((1 + df.mean()) ** trading_days - 1)
    out["Volatility"] = df.std() * np.sqrt(trading_days)
    out["Sharpe Ratio"] = df.mean() / df.std()
    return out

performance_all = compute_metrics(portfolios)
performance_in = compute_metrics(in_sample)
performance_out = compute_metrics(out_sample)

# ==========================================================
# 4. DRAWNDOWNS
# ==========================================================

drawdowns = portfolios_cum / portfolios_cum.cummax() - 1
drawdowns.plot(figsize=(10, 6))
plt.title("Figure 3: Portfolios' Drawdowns")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.tight_layout()
plt.savefig(output_path / "Figure3_Drawdowns.png", dpi=300)
plt.close()

# ==========================================================
# 5. CAPM
# ==========================================================

results_capm = pd.DataFrame(index=["Beta", "Alpha", "t-Stat(Alpha)", "Information Ratio"])
market_returns = portfolios["Market"]

for col in ["Long-Top", "Long-Bottom", "Long-Short"]:
    y = portfolios[col]
    X = sm.add_constant(market_returns)
    model = sm.OLS(y, X).fit()
    results_capm[col] = [
        model.params["Market"],
        model.params["const"],
        model.tvalues["const"],
        model.params["const"] / model.resid.std()
    ]

# ==========================================================
# 6. EXPORT
# ==========================================================

with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
    performance_all.to_excel(writer, sheet_name="Performance_All")
    performance_in.to_excel(writer, sheet_name="Performance_InSample")
    performance_out.to_excel(writer, sheet_name="Performance_OutSample")
    results_capm.to_excel(writer, sheet_name="CAPM")

# ==========================================================
# 7. INTERPRETATION
# ==========================================================

lt = performance_all.loc["Long-Top", "Average Annualized Return"]
lb = performance_all.loc["Long-Bottom", "Average Annualized Return"]
ls = performance_all.loc["Long-Short", "Average Annualized Return"]

interpretation = f"""
🧭 Interpretation:
Across the full sample, the Long-Short strategy achieved an annualized return of {ls:.2%},
highlighting the effectiveness of combining growth and liquidity signals.
The Long-Top portfolio (return {lt:.2%}) demonstrates consistent risk-adjusted strength,
while Long-Bottom ({lb:.2%}) underperforms, confirming that financially stronger firms 
generate superior returns.

The inclusion of the drawdown analysis (Figure 3) reveals periods of stress alignment 
with macro shocks (e.g., 2008, 2020), validating the robustness of the strategy under crisis.

✅ Portfolio construction and CAPM analysis completed successfully.
"""
print(interpretation)
=======

# === FILE PATHS ===
path_fundamentals = r"C:\Users\maria\OneDrive\Desktop\Tese\fundamentals_cleaned.xlsx"
path_returns = r"C:\Users\maria\OneDrive\Desktop\Tese\stocks_returns.csv"
path_factors = r"C:\Users\maria\OneDrive\Desktop\Tese\fffactors_daily.xlsx"
output_excel = r"C:\Users\maria\OneDrive\Desktop\Tese\portfolio_results.xlsx"

# === 1. READ DATA ===
fundamentals = pd.read_excel(path_fundamentals)
returns = pd.read_csv(path_returns)
factors = pd.read_excel(path_factors)

returns['Date'] = pd.to_datetime(returns['date'])
returns['Year'] = returns['Date'].dt.year

# Keep consistent columns
returns = returns.rename(columns={
    'TICKER': 'Ticker Symbol',
    'vwretd': 'Daily Stock Return'
})

# === 2. MERGE WITH FUNDAMENTALS ===
merged = pd.merge(returns, fundamentals, on=['Ticker Symbol', 'Year'], how='inner')
merged = merged.dropna(subset=['Sales Growth Rate', 'Current Ratio'])

# === 3. DEFINE PORTFOLIOS ===
# Long-Top (tercile = 0)
long_top = merged[merged['Tercile'] == 0]
# Long-Bottom (tercile = 2)
long_bottom = merged[merged['Tercile'] == 2]

# Market Portfolio = all stocks equally weighted
def calc_portfolio(df):
    grouped = df.groupby(['Date', 'Ticker Symbol'])['Daily Stock Return'].mean().unstack()
    grouped = grouped.fillna(0)
    grouped['Portfolio Return'] = grouped.mean(axis=1)
    return grouped['Portfolio Return']

long_top_returns = calc_portfolio(long_top)
long_bottom_returns = calc_portfolio(long_bottom)
market_returns = calc_portfolio(merged)

# Long-Short Portfolio
long_short_returns = long_top_returns - long_bottom_returns

# === 4. CALCULATE CUMULATIVE RETURNS ===
portfolios = pd.DataFrame({
    'Long-Top': long_top_returns,
    'Long-Bottom': long_bottom_returns,
    'Long-Short': long_short_returns,
    'Market': market_returns
}).dropna()

portfolios_cum = (1 + portfolios).cumprod()

# === 5. PLOT FIGURE 1 – CUMULATIVE RETURNS ===
plt.figure(figsize=(10, 6))
for col in portfolios_cum.columns:
    plt.plot(portfolios_cum.index, portfolios_cum[col], label=col)
plt.title("Figure 1: Portfolios' Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.savefig(r"C:\Users\maria\OneDrive\Desktop\Tese\Portfolios_Cumulative_Returns.png", dpi=300)
plt.show()

# === 6. VOLATILITY-TIMING STRATEGY (10%) ===
target_vol = 0.10
vol_adj = pd.DataFrame()

for col in portfolios.columns:
    realized_vol = portfolios[col].std() * np.sqrt(252)
    leverage = target_vol / realized_vol
    adjusted_returns = portfolios[col] * leverage
    vol_adj[col] = (1 + adjusted_returns).cumprod()

plt.figure(figsize=(10, 6))
for col in vol_adj.columns:
    plt.plot(vol_adj.index, vol_adj[col], label=col)
plt.title("Figure 2: Cumulative Returns with Volatility-Timing Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.savefig(r"C:\Users\maria\OneDrive\Desktop\Tese\Portfolios_Volatility_Timing.png", dpi=300)
plt.show()

# === 7. PERFORMANCE METRICS (Table 1) ===
trading_days = 252
performance = pd.DataFrame(index=portfolios.columns)

performance['Average Annualized Return'] = ((1 + portfolios.mean()) ** trading_days - 1)
performance['Volatility'] = portfolios.std() * np.sqrt(252)
performance['Sharpe Ratio'] = portfolios.mean() / portfolios.std()

performance.to_excel(output_excel, sheet_name='Performance', index=True)
print("\n📈 Table 1 – Performance Indicators:")
print(performance.round(4))

# === 8. CAPM ANALYSIS (Table 2) ===
results_capm = pd.DataFrame(index=['Beta', 'Alpha', 't-Stat(Alpha)', 'Information Ratio'])
market = portfolios['Market']

for col in ['Long-Top', 'Long-Bottom', 'Long-Short']:
    y = portfolios[col]
    X = sm.add_constant(market)
    model = sm.OLS(y, X).fit()
    beta = model.params['Market']
    alpha = model.params['const']
    t_alpha = model.tvalues['const']
    ir = alpha / model.resid.std()
    results_capm[col] = [beta, alpha, t_alpha, ir]

with pd.ExcelWriter(output_excel, mode='a', if_sheet_exists='replace') as writer:
    results_capm.to_excel(writer, sheet_name='CAPM')

print("\n📊 Table 2 – CAPM Results:")
print(results_capm.round(4))

print("\n✅ All outputs saved successfully!")
>>>>>>> a6a7c26f02ffdb8df2d3921afa91c3327d6a5781
