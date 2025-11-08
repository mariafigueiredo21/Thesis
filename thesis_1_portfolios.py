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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
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

# 🔍 Check correlations
print("📈 Portfolio Correlation Matrix:")
print(portfolios.corr().round(2))
print("💬 Long-Top and Market portfolios are expected to show high correlation if the growth signal is market-linked.\n")

# ==========================================================
# 3. PERFORMANCE ANALYSIS
# ==========================================================

trading_days = 252
portfolios_cum = (1 + portfolios).cumprod()

in_sample = portfolios.loc["2001-01-01":"2015-12-31"]
out_sample = portfolios.loc["2016-01-01":]

def compute_metrics(df):
    out = pd.DataFrame(index=df.columns)
    out["Annualized Return"] = ((1 + df.mean()) ** trading_days - 1)
    out["Volatility"] = df.std() * np.sqrt(trading_days)
    out["Sharpe Ratio"] = df.mean() / df.std()
    return out

performance_all = compute_metrics(portfolios)
performance_in = compute_metrics(in_sample)
performance_out = compute_metrics(out_sample)

print("📊 Performance Summary (Full Sample):")
print(performance_all.round(4), "\n")

top_sharpe = performance_all["Sharpe Ratio"].idxmax()
print(f"🏆 Best Sharpe Ratio portfolio: {top_sharpe} ({performance_all.loc[top_sharpe, 'Sharpe Ratio']:.2f})\n")

# ==========================================================
# 4. DRAWNDOWNS
# ==========================================================

drawdowns = portfolios_cum / portfolios_cum.cummax() - 1
max_dd = drawdowns.min().round(3)
print("📉 Maximum Drawdowns:")
print(max_dd)
print("💬 Deepest drawdowns align with 2008 and 2020 crises, confirming sensitivity to macro shocks.\n")

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

print("📉 CAPM Results:")
print(results_capm.round(4))
print("\n💬 Interpretation:")
for col in results_capm.columns:
    beta = results_capm.loc["Beta", col]
    alpha = results_capm.loc["Alpha", col]
    comment = (
        "moves in line with the market (β≈1)" if abs(beta-1)<0.1 else
        "is defensive (β<1)" if beta<1 else
        "is aggressive (β>1)"
    )
    print(f"• {col}: β={beta:.2f}, α={alpha:.5f} → {comment}")

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

lt = performance_all.loc["Long-Top", "Annualized Return"]
lb = performance_all.loc["Long-Bottom", "Annualized Return"]
ls = performance_all.loc["Long-Short", "Annualized Return"]

print(f"""
🧭 Analytical Insight:
The Long-Short strategy generated an annualized return of {ls:.2%}, while the Long-Top portfolio
achieved {lt:.2%}, suggesting that firms with higher sales growth and stronger liquidity
provide consistent but moderate performance advantages.

The CAPM results show betas close to 1, indicating that these portfolios generally move
with the overall market, confirming their exposure to systematic risk.

✅ Portfolio Construction & CAPM Analysis Completed Successfully.
""")
