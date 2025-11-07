# ----------------------------------------------------------
# Thesis Project – Part 1: Data Preparation
# Author: Maria C. F. Figueiredo
# Master’s in Finance – Nova SBE
# ----------------------------------------------------------

import pandas as pd
import numpy as np

# === FILE PATHS ===
path_financials = r"C:\Users\maria\OneDrive\Desktop\Tese\financial_data_1.xlsx"
path_tickers = r"C:\Users\maria\OneDrive\Desktop\Tese\tickers.xlsx"
output_path = r"C:\Users\maria\OneDrive\Desktop\Tese\fundamentals_cleaned.xlsx"

# === 1. READ DATA ===
data = pd.read_excel(path_financials)
tickers = pd.read_excel(path_tickers)

# Keep only relevant tickers
data = data[data['Ticker Symbol'].isin(tickers['Tickers'])]

# === 2. CLEAN DATA ===
columns_to_drop = [
    'Global Company Key',
    'Data Year - Fiscal',
    'Earnings Per Share (Diluted) - Excluding Extraordinary Items'
]
data = data.drop(columns=[c for c in columns_to_drop if c in data.columns])

# Convert and extract year
data['DATE'] = pd.to_datetime(data['Data Date'])
data['Year'] = data['DATE'].dt.year
data = data[data['Year'] <= 2022]

# === 3. CALCULATE FINANCIAL RATIOS ===
data['Current Ratio'] = (
    data['Current Assets - Total'] / data['Current Liabilities - Total']
)

# Sales Growth Rate (annual)
data = data.sort_values(by=['Ticker Symbol', 'Year'])
data['Sales Growth Rate'] = data.groupby('Ticker Symbol')['Sales/Turnover (Net)'].pct_change()
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data = data.dropna(subset=['Sales Growth Rate', 'Current Ratio'])

# === 4. CREATE RANKINGS AND TERCILES ===
data = data.sort_values(by=['Year', 'Sales Growth Rate', 'Current Ratio'], ascending=[True, False, False])

data['Rank_Combined'] = data.groupby('Year') \
    .apply(lambda x: x[['Sales Growth Rate', 'Current Ratio']]
           .mean(axis=1)
           .rank(ascending=False)) \
    .reset_index(level=0, drop=True)

def assign_tercile(series):
    tercile = pd.qcut(series, 3, labels=[0, 1, 2])
    return tercile

data['Tercile'] = data.groupby('Year')['Rank_Combined'].transform(assign_tercile)
data['Tercile'] = data['Tercile'].astype(int)

# Keep only years with valid data
data = data[(data['Year'] >= 2000) & (data['Year'] <= 2022)]

# === 5. EXPORT CLEANED DATA ===
data.to_excel(output_path, index=False)
print(f"✅ Fundamentals cleaned and saved to: {output_path}")

# Preview
print(data[['Ticker Symbol', 'Year', 'Sales Growth Rate', 'Current Ratio', 'Tercile']].head(10))
