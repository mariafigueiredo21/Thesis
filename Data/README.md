# 🗂️ Thesis Project — Part 1: Data Preparation and Financial Signal Construction

### 📘 Overview

This directory contains all raw and processed datasets used in the first stage of the thesis:
Data Preparation and Financial Signal Construction.
It provides the empirical foundation for building and testing the financial signals — Sales Growth and Liquidity (Current Ratio) — used in portfolio formation and performance evaluation.
The accompanying Python script preview_data.py automatically scans all files, prints descriptive statistics (shape, columns, missing values), previews the first rows, and provides a concise academic interpretation for each dataset.
---

### ⚙️ Script's Purpose
The purpose of this script is to automatically inspect all datasets in this folder and print structured information and academic interpretations for each file.
This tool was designed to ensure transparency, consistency, and traceability in the data collection and preprocessing phase of the thesis.

### 📊 Datasets and Interpretations 
#### - fffactors_daily.xlsx
  - Contains the daily Fama–French factors (Market–RF, SMB, HML, RF) used as the benchmark model for performance adjustment and regression analysis. It forms the foundation for estimating abnormal returns (alphas) in portfolio tests.
#### - financial_data_1.xlsx
  - Comprehensive firm-level dataset from Compustat/CRSP including balance sheet and income statement variables (assets, liabilities, sales, EPS). Serves as the raw input for computing fundamental ratios and signals used in portfolio formation.
#### - fundamentals_cleaned.xlsx
  - Cleaned and structured version of the financial data, containing calculated ratios such as Current Ratio and Sales Growth Rate, along with composite signal ranks and tercile classifications.
  - It represents the core dataset used for empirical analysis and portfolio construction.
#### - portfolio_results.xlsx
  - Summarizes annualized performance metrics (return, volatility, Sharpe ratio) for the constructed portfolios. Provides the first quantitative assessment of the risk–return trade-off among the Long–Top, Long–Bottom, and Long–Short strategies.
#### - stocks_returns.csv
  - Massive panel of daily stock-level returns with identifiers (PERMNO, ticker, price, return, market return). Forms the empirical backbone for calculating portfolio returns and conducting cross-sectional performance tests.
#### - tickers.xlsx
  - List of all tickers (firm identifiers) in the analysis universe, ensuring data consistency across financial, returns, and portfolio datasets. Functions as a linking table between sources.

### 🧠 Research Context
The datasets in this folder collectively enable the empirical reconstruction of firm fundamentals and market behavior across the 2000–2023 sample period.
They serve to:
- Compute financial signals capturing growth and liquidity characteristics.
- Build ranking-based portfolios (Long–Top, Long–Bottom, Long–Short).
- Enable factor-adjusted performance evaluation via Fama–French regressions.
This structured data foundation ensures methodological transparency and reproducibility of all subsequent analyses in the thesis.

### ✅ Version Information
- Script version: v1.0 (Final)
- Date generated: November 2025
- Language: Python 3.11
- Dependencies: pandas, json, pathlib
