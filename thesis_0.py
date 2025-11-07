# thesis_0_annual.py — Quant Thesis Project
# Author: Maria Simões
# Versão: dados anuais + top 50 Nasdaq-100 (lista fixa)

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import warnings

# ------------------------------------------------
# 0. Configuração inicial
# ------------------------------------------------
warnings.simplefilter(action='ignore', category=FutureWarning)

start = dt.datetime(2015, 1, 1)
end = dt.datetime(2024, 12, 31)

# ------------------------------------------------
# 1. Lista fixa — top 50 da NASDAQ-100
# ------------------------------------------------
tickers = [
    'AAPL','MSFT','AMZN','NVDA','GOOG','META','TSLA','PEP','COST','NFLX',
    'AVGO','ADBE','AMD','CSCO','INTC','TXN','HON','INTU','AMAT','QCOM',
    'PYPL','AMGN','MU','MDLZ','ADP','SBUX','BKNG','CHTR','LRCX','GILD',
    'ISRG','REGN','KLAC','PANW','MAR','CSX','MRNA','ABNB','CDNS','FTNT',
    'SNPS','AEP','KDP','ADSK','VRTX','PDD','NXPI','MELI','CRWD','CTAS'
]
print(f"Selecionadas {len(tickers)} empresas (lista fixa).")
print(tickers[:10], "…\n")

# ------------------------------------------------
# 2. Obter preços históricos (para controlo)
# ------------------------------------------------
print("📥 A descarregar dados de preços (para controlo)...")
data = yf.download(tickers, start=start, end=end, group_by='ticker', interval='1d', auto_adjust=True)
print("✅ Dados de preços carregados com sucesso.\n")

# ------------------------------------------------
# 3. Obter dados fundamentais anuais
# ------------------------------------------------
fundamentals = []
print("📊 A processar dados fundamentais (anuais)...")

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        income_y = stock.financials.T       # demonstração de resultados anual
        balance_y = stock.balance_sheet.T   # balanço anual

        # garantir que temos as colunas necessárias
        if {'Total Revenue', 'Current Assets', 'Current Liabilities'}.issubset(balance_y.columns.union(income_y.columns)):
            df = pd.DataFrame({
                'Sales': income_y['Total Revenue'],
                'CurrentAssets': balance_y['Current Assets'],
                'CurrentLiabilities': balance_y['Current Liabilities']
            })
            df['Ticker'] = ticker
            fundamentals.append(df)
    except Exception as e:
        print(f"⚠️ Falha ao obter {ticker}: {e}")

# Concatenar todas as empresas
fundamentals = pd.concat(fundamentals)
fundamentals.index = pd.to_datetime(fundamentals.index)
fundamentals.sort_index(inplace=True)

# ------------------------------------------------
# 4. Calcular indicadores anuais
# ------------------------------------------------
fundamentals['SalesGrowth'] = fundamentals.groupby('Ticker')['Sales'].pct_change(fill_method=None)
fundamentals['CurrentRatio'] = fundamentals['CurrentAssets'] / fundamentals['CurrentLiabilities']

# Limpeza básica
fundamentals = fundamentals.dropna(subset=['SalesGrowth', 'CurrentRatio'])
fundamentals = fundamentals[(fundamentals['SalesGrowth'] > -1) & (fundamentals['SalesGrowth'] < 5)]

print("\n✅ Indicadores anuais calculados com sucesso!")
print(fundamentals[['Ticker', 'Sales', 'SalesGrowth', 'CurrentRatio']].head(10))

# ------------------------------------------------
# 5. Criar rankings anuais
# ------------------------------------------------
print("\n🏗️ A construir rankings e portfólios (anuais)...")

# Criar coluna com o ano
fundamentals['Year'] = fundamentals.index.to_period('Y')

# Função de ranking
def rank_by_signal(df, signal):
    df = df.copy()
    df['Rank_' + signal] = pd.qcut(df[signal], 3, labels=False, duplicates='drop')
    return df

# Aplicar rankings
fundamentals = fundamentals.groupby('Year', group_keys=False).apply(rank_by_signal, 'SalesGrowth').reset_index(drop=True)
fundamentals = fundamentals.groupby('Year', group_keys=False).apply(rank_by_signal, 'CurrentRatio').reset_index(drop=True)

# Ranking combinado
fundamentals['Rank_Combined'] = (
    fundamentals['Rank_SalesGrowth'] + fundamentals['Rank_CurrentRatio']
) / 2
fundamentals['Rank_Combined'] = pd.qcut(
    fundamentals['Rank_Combined'], 3, labels=False, duplicates='drop'
)

print("✅ Rankings anuais criados com sucesso!\n")
print(
    fundamentals[
        ['Ticker', 'Year', 'Rank_SalesGrowth', 'Rank_CurrentRatio', 'Rank_Combined']
    ].head(10)
)

# ------------------------------------------------
# 6. Guardar dataset
# ------------------------------------------------
fundamentals.to_pickle('fundamentals_annual.pkl')
print("\n💾 Dados anuais guardados em 'fundamentals_annual.pkl'.")
print("\n✅ Tudo pronto para a próxima fase: construção dos portfólios!")
