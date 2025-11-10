
# 📊 Thesis Project — Part 2: Output Analysis and Empirical Interpretation

## 📘 Overview

This directory contains all generated outputs, including portfolio performance tables, econometric model results, and illustrative figures produced throughout the empirical stages of the thesis.
It represents the culmination of the Data Preparation and Signal Construction phases, integrating quantitative results, statistical diagnostics, and visual analytics.
The accompanying Python script, preview_output.py, automatically scans all files in this directory, classifies them by type (Excel/CSV reports or figures), and prints structured interpretations for each output.

---

## ⚙️ Script's Purpose
The purpose of this script is to provide an automated and standardized interpretation of all empirical outputs generated during the thesis project — covering descriptive analyses, portfolio performance metrics, factor model estimations, and graphical results.

## 🧾 Output Categories and Interpretations
### 🧩 Graphical Outputs
#### Figure 0_Distribution Signals
  - Visualizes the relationship between Sales Growth and Current Ratio across terciles, revealing that liquidity varies more widely than growth and that high-growth firms do not necessarily exhibit higher liquidity.
#### Figure 1_Cumulative Returns
  - Displays cumulative returns for Long–Top, Long–Bottom, Long–Short, and Market portfolios (2000–2023). Market-exposed portfolios dominate, while the Long–Short remains flat, highlighting weak cross-sectional predictability..
#### Figure 2_Volatility Timing
  - Shows cumulative returns under volatility-timing. Confirms that scaling exposure enhances stability but does not change relative performance ranking — market portfolios still outperform.
#### Figure 3_Drawdowns
  - Presents drawdown profiles of all portfolios, emphasizing the defensive nature of the Long–Short strategy during crises and the risk–return trade-off for the Market portfolio.
#### Figure_Conditional Drawdowns
  - Depicts cumulative conditional losses, confirming the resilience of the Long–Short portfolio during systemic shocks (2008, 2020, 2022).
#### Figure_Factor_Correlation_Heatmap
  - Shows the correlation matrix among portfolios and Fama–French factors, confirming high market co-movement and weak exposure to size and value factors.
#### Figure_FF Comparison
  - Compares Fama–French 3- and 5-Factor model alphas, showing minimal differences and reinforcing that profitability and investment factors add limited explanatory power.
#### Figure_FF Stability
  - Compares in- and out-of-sample alphas from FF3 regressions, showing persistent negative alphas but reduced magnitude post-2016 — evidence of stable model performance.
#### Figure_Regime_Performance
  - Summarizes portfolio performance across economic regimes, highlighting improvement after crises and gradual stabilization over time.
#### Figure_RollingAlpha
  - Shows 3-year rolling alphas, revealing post-2011 improvements and a convergence of portfolio trajectories driven by systematic risk.
#### Figure_RollingR2
  - Displays rolling R² evolution, confirming that factor models explain a modest share of returns, with increased co-movement during stress periods.
#### Figure_Volatility_Timing
  - Demonstrates cumulative returns of volatility-targeted portfolios at σ = 10%, reinforcing that volatility targeting smooths risk but does not generate new alpha.

### 📁 Data Outputs
#### downside_risk_metrics
  - Contains key downside risk metrics (Sharpe, Sortino, Omega, CDaR) for each portfolio, enabling comparison of efficiency and stability across strategies.
#### factor_correlation_matrix
  - Provides correlations between portfolios and Fama–French factors, confirming that Long–Short behaves inversely to market-oriented exposures.
#### fama_french_inout
  - Reports in- and out-of-sample regression estimates from the Fama–French 3-Factor model, validating temporal robustness of alphas and betas.
#### fama_french_results
  - Presents the main FF3 regression results, confirming that alphas are statistically insignificant once systematic risks are controlled for.
#### fama_macbeth_results
  - Summarizes cross-sectional Fama–MacBeth regressions, testing the pricing relevance of growth and liquidity betas across firms.
#### fundamentals_cleaned
  - Provides firm-level accounting variables and computed signals forming the empirical base for portfolio ranking and performance testing.
#### performance_by_regime
  - Summarizes portfolio performance across macroeconomic regimes (pre-crisis, crisis, recovery, post-COVID), revealing dynamic shifts in risk-adjusted returns.
#### portfolio_daily_returns
  - Contains daily returns for all portfolios and the market (2000–2023), serving as the core dataset for performance and factor regressions.
#### portfolio_results
  - Reports annualized performance metrics (return, volatility, Sharpe ratio), synthesizing the risk–return characteristics of each portfolio.
#### rolling_regression_results
  - Provides rolling regression outputs (alphas) across 3-year windows, capturing time-varying performance dynamics.
#### summary_stats
  - Offers descriptive statistics for the main financial ratios, defining the initial data structure and supporting the tercile classification.
#### volatility_timing_results
  - Contains the time series of returns for volatility-targeted portfolios, underpinning the analysis of risk-managed performance.
    
## 🧠 Research Context
The outputs in this folder collectively provide the empirical evidence for the thesis’ quantitative findings.
They illustrate how the Sales Growth × Liquidity signal interacts with systematic risk, market regimes, and volatility, confirming that:
- Portfolio performance is largely explained by common risk factors (Fama–French).
- The Long–Short strategy offers stability and low drawdowns, but limited alpha generation.
- Volatility targeting improves risk control without altering performance rankings.
- Post-crisis market environments exhibit stronger convergence and resilience among strategies.
Together, these outputs form the quantitative core of the thesis’ empirical validation.

### ✅ Version Information
- Script version: v1.0 (Final)
- Date generated: November 2025
- Language: Python 3.11
- Dependencies: pandas, PIL, datetime, pathlib, os
