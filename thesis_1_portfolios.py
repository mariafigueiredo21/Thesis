# thesis_1_portfolios_annual.py — Quant Thesis Project
# Parte 7: Construção e análise dos portfólios anuais
# Author: Maria Simões

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# ------------------------------------------------
# 1. Carregar os dados fundamentais anuais
# ------------------------------------------------
fundamentals = pd.read_pickle('fundamentals_annual.pkl')

# Extrair variáveis de referência (tickers, datas)
tickers = fundamentals['Ticker'].unique().tolist()
start = dt.datetime(2015, 1, 1)
end = dt.datetime(2024, 12, 31)

print("✅ Dados fundamentais carregados para construção dos portfólios.\n")

# ------------------------------------------------
# 2. Obter preços ajustados anuais
# ------------------------------------------------
print("📥 A descarregar preços anuais...")

prices = yf.download(tickers, start=start, end=end, interval='1mo', auto_adjust=True)['Close']
prices = prices.resample('Y').last()  # último preço de cada ano

# Calcular retornos anuais
returns = prices.pct_change()
returns.index = returns.index.to_period('Y')

print("✅ Retornos anuais calculados com sucesso.\n")

# ------------------------------------------------
# 3. Combinar rankings e retornos
# ------------------------------------------------
# Juntar o ranking do ano com o retorno do ano seguinte
fundamentals = fundamentals.copy()
fundamentals['YearNext'] = fundamentals['Year'] + 1  # alinhar retorno futuro

merged = fundamentals.merge(
    returns.stack().rename('Return').reset_index().rename(columns={'level_1': 'Ticker', 'Date': 'Year'}),
    left_on=['Ticker', 'YearNext'],
    right_on=['Ticker', 'Year'],
    how='inner'
)

print("✅ Dados combinados com retornos futuros e rankings anuais.\n")
print(merged[['Ticker', 'Year_x', 'Rank_Combined', 'Return']].head())

# ------------------------------------------------
# 4. Criar portfólios anuais
# ------------------------------------------------
def portfolio_return(df, rank):
    """Calcula o retorno médio do portfólio para um dado rank (0,1,2)."""
    port = df[df['Rank_Combined'] == rank].groupby('Year_x')['Return'].mean()
    return port

port_top = portfolio_return(merged, 2)
port_mid = portfolio_return(merged, 1)
port_bot = portfolio_return(merged, 0)

# Portfólio long-short (Top - Bottom)
port_ls = port_top - port_bot

# Combinar todos
portfolios = pd.concat(
    [port_top, port_mid, port_bot, port_ls], axis=1
)
portfolios.columns = ['Top (Rank 2)', 'Middle (Rank 1)', 'Bottom (Rank 0)', 'Long-Short (Top-Bottom)']

print("\n✅ Portfólios construídos com sucesso!")
print(portfolios.tail())

# ------------------------------------------------
# 5. Calcular métricas de performance
# ------------------------------------------------
def performance_metrics(returns):
    avg_ret = returns.mean()      # média anual
    vol = returns.std()
    sharpe = avg_ret / vol if vol != 0 else np.nan
    return avg_ret, vol, sharpe

print("\n📊 Métricas de performance (anuais):")
metrics = pd.DataFrame(
    [performance_metrics(portfolios[c]) for c in portfolios.columns],
    index=portfolios.columns,
    columns=['Return', 'Volatility', 'Sharpe']
)
print(metrics.round(3))

# ------------------------------------------------
# 6. Plotar performance acumulada
# ------------------------------------------------
cum_returns = (1 + portfolios).cumprod()

plt.figure(figsize=(12,6))
plt.plot(cum_returns.index.to_timestamp(), cum_returns['Top (Rank 2)'], label='Top (Rank 2)', linewidth=2)
plt.plot(cum_returns.index.to_timestamp(), cum_returns['Bottom (Rank 0)'], label='Bottom (Rank 0)', linestyle='--')
plt.plot(cum_returns.index.to_timestamp(), cum_returns['Long-Short (Top-Bottom)'], label='Long-Short', linewidth=2, color='black')

plt.title("📈 Performance Acumulada dos Portfólios Fundamentais (Anual)", fontsize=13)
plt.ylabel("Crescimento do Investimento (base = 1.0)")
plt.xlabel("Ano")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n✅ Análise de portfólios concluída com sucesso!")
