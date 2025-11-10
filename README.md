# 🎓 Thesis Project – Empirical Rebuild

Sales Growth × Liquidity Framework

Master’s Thesis in Finance – Nova School of Business and Economics

Author: Maria Cevadinha Simões Figueiredo

Supervisor: Prof. Nicholas Hirschey

Date: November 2025
---

## 📘 Overview

This project reconstructs, in a fully reproducible Python framework, the empirical foundation of the Sales Growth × Liquidity investment signal.
It explores whether these fundamental indicators — proxies for firm quality and financial stability — generate persistent abnormal returns or simply reflect priced systematic risk.

The analysis integrates modern asset-pricing theory and quantitative portfolio construction, combining data preparation, signal engineering, factor regressions, and multi-layer robustness checks.
Each module contributes a piece of the full empirical narrative, from raw accounting data to risk-adjusted performance validation.

## 🧠 Theoretical Foundation
The thesis builds upon established literature in empirical asset pricing:
- Fama & French (1993, 2015): multi-factor models explaining cross-sectional returns.
- Moreira & Muir (2017): volatility-managed portfolios as a robustness framework.
- Fama & MacBeth (1973): cross-sectional tests for factor premia.
- Frazzini & Pedersen (2014): “Quality Minus Junk” factor as a quality-based benchmark.

The central hypothesis:
- Firms with higher sales growth and stronger liquidity ratios behave as “quality firms” — stable and efficient, but not systematically mispriced.

## ⚙️ Analytical Structure
#### 1️⃣ Data Preparation
  - The focus is Signal Construction
  - The objective is to clean Compustat data, compute Sales Growth and Current Ratio, and classify firms into terciles.
#### 2️⃣ Portfolio Construction
  - The focus is Performance Analysis
  - The objective is to build Long–Top, Long–Bottom, and Long–Short portfolios; estimate Sharpe ratios and drawdowns.
#### 3️⃣ Multi-Factor Models
  - The focus is Fama–French 3 & 5 Factors
  - The objective is to test whether returns are explained by systematic risk exposures (MKT, SMB, HML, RMW, CMA).
#### 4️⃣ Volatility Targeting
  - The focus is Risk Normalization
  - The objective is to apply volatility scaling (σ = 10%) to assess robustness across regimes.
#### 5️⃣ Advanced Robustness
  - The focus is Rolling & Cross-Sectional Tests
  - The objective is to Evaluate temporal and cross-sectional stability (Fama–MacBeth, downside risk).
#### Annex A & B
  - The focus is Regime & Correlation Analysis
  - The objective is to Examine regime-dependent performance and correlation with canonical factors.

## 🔍 Key Empirical Insights
#### 1. Systematic Risk Dominance:
  - Portfolio alphas are statistically insignificant once Fama–French factors are included — confirming that performance stems from common risk exposures, not anomalies.
#### 2. Quality–Defensive Behaviour:
  - The Long–Short spread behaves as a defensive, counter-cyclical quality factor — stable during crises, flat during expansions.
#### 3. Volatility-Managed Robustness:
  - Volatility targeting (σ = 10%) enhances return stability without creating alpha, reinforcing market efficiency.
#### 4. Cross-Sectional Neutrality:
  - Fama–MacBeth regressions show no persistent premia on growth or liquidity — these variables describe firm quality, not priced risk.
#### 5. Regime Consistency:
  - Results remain stable across pre-crisis, crisis, recovery, and post-COVID regimes, highlighting structural resilience.

## 📊 Methodological Highlights
- Data Source: Compustat Global (2000–2022) and Kenneth French’s Data Library.
- Estimation Framework: OLS regressions (time-series & cross-sectional), rolling windows, volatility-scaling, and downside risk metrics.
- Key Tools: pandas, statsmodels, matplotlib, seaborn, scipy.
- Output: Excel datasets, figures (α, R², drawdowns), and textual analytical summaries.

## 🧩 Interpretation
The integrated results demonstrate that the Sales Growth × Liquidity framework is:
- Statistically persistent — signals remain stable across time and regimes;
- Economically neutral — excess returns vanish under risk-adjusted models;
- Qualitatively meaningful — captures firm stability rather than mispricing.

“Strong fundamentals explain strong firms — not necessarily excess returns.”

---

### ✅ Project Summary
- Analytical pipeline: 7 Python modules (Parts 1–5 + Annexes A–B)
- Automated synthesis: via thesis_rebuild.py
- Core outcome: A fully reproducible, factor-based empirical validation of the quality dimension in asset pricing.
