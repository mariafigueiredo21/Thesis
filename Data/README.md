# 📁 Thesis Project — Data Folder

This directory contains all **raw, intermediate, and processed datasets** used in the empirical analysis of the quantitative strategy **Sales Growth × Liquidity**.  
Each file supports a specific stage of the workflow — from firm fundamentals to portfolio construction and risk-adjusted evaluation.

---

## 🧩 Dataset Descriptions

### 1️⃣ `fffactors_daily.xlsx`
**Purpose:** Benchmark risk factors for regression and performance attribution (Fama–French 3/5).  
**Source:** Kenneth R. French Data Library.  
**Frequency:** Daily  
**Shape:** 5,787 rows × 5 columns  
**Columns:**  
- `Date` — Trading date (DD-MM-YYYY)  
- `Mkt-RF` — Market excess return  
- `SMB` — Small Minus Big size factor  
- `HML` — High Minus Low value factor  
- `RF` — Risk-free rate (%)  
**Missing values:** 0  

🧠 *Used in:* multi-factor regression models and alpha estimation.

---

### 2️⃣ `financial_data_1.xlsx`
**Purpose:** Raw firm-level financials used to construct sales growth and liquidity ratios.  
**Source:** Refinitiv/Compustat style extract.  
**Frequency:** Annual (fiscal year)  
**Shape:** 261,951 rows × 9 columns  
**Columns (main):**  
- `Global Company Key`, `Data Date`, `Data Year - Fiscal`, `Ticker Symbol`, `Company Name`  
- `Current Assets - Total`, `Current Liabilities - Total`  
- `Earnings Per Share (Diluted) - Excluding Extraordinary Items`  
- `Sales/Turnover (Net)`  
**Missing values:** 296,085  

🧠 *Used in:* computation of financial ratios and sales/liquidity signals.

---

### 3️⃣ `fundamentals_cleaned.xlsx`
**Purpose:** Cleaned dataset after filtering, winsorization, and ratio calculation.  
**Source:** Output from preprocessing script `thesis_0.py`  
**Frequency:** Annual  
**Shape:** 25,625 rows × 12 columns  
**Columns (key):**  
- `Data Date`, `Ticker Symbol`, `Company Name`, `DATE`, `Year`  
- `Current Ratio` — liquidity metric  
- `Sales Growth Rate` — sales momentum metric  
- `Rank_Combined` — composite score combining growth & liquidity  
- `Tercile` — portfolio allocation (0 = Low, 1 = Mid, 2 = High)  
**Missing values:** 4  

🧠 *Used in:* portfolio construction and signal ranking.

---

### 4️⃣ `portfolio_results.xlsx`
**Purpose:** Summary of performance metrics for the constructed portfolios.  
**Source:** Output from portfolio evaluation script (`thesis_2.py`).  
**Frequency:** Aggregate (portfolio-level summary).  
**Shape:** 4 rows × 4 columns  
**Columns:**  
- `Average Annualized Return`  
- `Volatility`  
- `Sharpe Ratio`  
**Missing values:** 0  

🧠 *Used in:* final performance comparison (Long–Top, Long–Bottom, Long–Short).

---

### 5️⃣ `stocks_returns.csv`
**Purpose:** Daily stock-level market data used to compute portfolio returns.  
**Source:** CRSP-like dataset (Compustat/Refinitiv).  
**Frequency:** Daily  
**Shape:** 42,561,675 rows × 6 columns  
**Columns:**  
- `PERMNO` — unique stock identifier  
- `date` — trading date  
- `TICKER` — stock ticker  
- `PRC` — closing price  
- `RET` — daily return  
- `vwretd` — value-weighted market return  
**Missing values:** 1,244,931  

🧠 *Used in:* time-series alignment, excess return computation, and portfolio weighting.

---

### 6️⃣ `tickers.xlsx`
**Purpose:** Master list of valid tickers in the sample universe.  
**Frequency:** Static  
**Shape:** 3,521 rows × 1 column  
**Column:** `Tickers`  
**Missing values:** 1  

🧠 *Used in:* filtering and cross-checking tickers across datasets.

---

## ⚙️ Utility Script — `preview_data.py`
A small inspection utility that automatically scans the `Data/` folder and prints a compact summary of every dataset (shape, columns, missing values, and sample).



