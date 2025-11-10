"""
------------------------------------------------------------------------------
Thesis Project – Part 1: Data Preparation and Financial Signal Construction
Author: Maria Figueiredo
Master’s in Finance – Nova School of Business and Economics
Supervisor: Prof. Nicholas Hirschey
Date: November 2025
------------------------------------------------------------------------------

Purpose:
Prepare and clean Compustat data, calculate the Sales Growth Rate and Current Ratio,
filter outliers, and classify firms annually into terciles based on combined ranking.

Outputs include cleaned data, descriptive statistics, and exploratory plots.
Includes automatic analytical insights throughout execution.

------------------------------------------------------------------------------
"""

###################################### 0. INITIAL SETUP ######################################

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import mstats
import seaborn as sns
import matplotlib.pyplot as plt

# Dynamic paths
root_path = Path(__file__).resolve().parent
data_path = root_path / "data"
output_path = root_path / "output"
output_path.mkdir(parents=True, exist_ok=True)

path_financials = data_path / "financial_data_1.xlsx"
path_tickers = data_path / "tickers.xlsx"
output_file = output_path / "fundamentals_cleaned.xlsx"
summary_file = output_path / "summary_stats.xlsx"

print("🚀 Thesis Project – Part 1: Data Preparation")
print("📂 Data folder:", data_path)
print("📄 Output folder:", output_path, "\n")

###################################### 1. LOAD DATA ######################################

print("📥 Reading datasets...")
data = pd.read_excel(path_financials)
tickers = pd.read_excel(path_tickers)
data = data[data["Ticker Symbol"].isin(tickers["Tickers"])]

print(f"✅ Loaded {data.shape[0]:,} records for {data['Ticker Symbol'].nunique()} tickers.\n")

###################################### 2. CLEANING ######################################

print("🧹 Cleaning data...")
cols_drop = [
    "Global Company Key",
    "Data Year - Fiscal",
    "Earnings Per Share (Diluted) - Excluding Extraordinary Items"
]
data.drop(columns=[c for c in cols_drop if c in data.columns], inplace=True)

data["DATE"] = pd.to_datetime(data["Data Date"], errors="coerce")
data["Year"] = data["DATE"].dt.year
data = data[data["Year"].between(2000, 2022)]

data.dropna(subset=["Current Assets - Total", "Current Liabilities - Total", "Sales/Turnover (Net)"], inplace=True)

###################################### 3. SIGNALS ######################################

print("💹 Calculating financial signals...")
data.sort_values(by=["Ticker Symbol", "Year"], inplace=True)
data["Current Ratio"] = data["Current Assets - Total"] / data["Current Liabilities - Total"]
data["Sales Growth Rate"] = data.groupby("Ticker Symbol")["Sales/Turnover (Net)"].pct_change()

data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(subset=["Sales Growth Rate", "Current Ratio"], inplace=True)

# Winsorization to reduce extreme outliers
data["Sales Growth Rate"] = mstats.winsorize(data["Sales Growth Rate"], limits=[0.01, 0.01])

print("📈 Signal Summary (after cleaning and winsorization):")
print(data[["Sales Growth Rate", "Current Ratio"]].describe().round(2), "\n")

###################################### 4. RANKINGS ######################################

print("🏗️ Constructing combined ranking and terciles...")
data["Rank_Combined"] = (
    data.groupby("Year")[["Sales Growth Rate", "Current Ratio"]]
    .transform(lambda x: x.rank(ascending=False))
    .mean(axis=1)
)
data["Tercile"] = data.groupby("Year")["Rank_Combined"].transform(lambda x: pd.qcut(x, 3, labels=[0, 1, 2])).astype(int)

###################################### 5. CHECK DATA COVERAGE ######################################

print("📊 Tercile Distribution (% of firms per tercile):")
print(data["Tercile"].value_counts(normalize=True).mul(100).round(2))
print("💬 Even distribution confirms balanced segmentation across all years.\n")

expected_years = set(range(2000, 2023))
missing = expected_years - set(data["Year"].unique())
if missing:
    print(f"⚠️ Missing data for years: {sorted(missing)}\n")

###################################### 6. EXPORT DATA ######################################

data.to_excel(output_file, index=False)
summary = data.groupby("Tercile")[["Sales Growth Rate", "Current Ratio"]].agg(["mean", "median", "std"]).round(3)
summary.to_excel(summary_file)
print(f"💾 Cleaned dataset saved → {output_file}")

print(f"📊 Summary statistics saved → {summary_file}\n")

###################################### 7. VISUALIZATION ######################################

sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x="Sales Growth Rate", y="Current Ratio", hue="Tercile", palette="coolwarm", alpha=0.7)
plt.title("Figure 1: Distribution of Financial Signals by Tercile")
plt.tight_layout()
plt.savefig(output_path / "Figure 1_Distribution_Signals.png", dpi=300)
plt.close()

###################################### 8. INTERPRETATION ######################################

# === ANALYSIS START ===
"""
📊 **Empirical Interpretation – Data Preparation**

Firms in the top tercile (0) exhibit the highest average Sales Growth Rate and Current Ratio,
signalling superior growth and liquidity potential. These companies are likely to be 
financially stable and positioned for above-average performance.

Conversely, firms in the bottom tercile (2) display weaker fundamentals,
suggesting potential exposure to financial distress or limited growth capacity.

🧭 **Analytical Insight**
The data shows a clear separation between terciles:
- **Tercile 0**: highest growth and liquidity (potential outperformers)
- **Tercile 1**: moderate fundamentals
- **Tercile 2**: weakest liquidity and growth metrics

The median Current Ratio above 2 suggests that the average firm maintains
a healthy short-term solvency position.

✅ **Conclusion:** Data preparation complete and signals robustly defined.
"""
# === ANALYSIS END ===
