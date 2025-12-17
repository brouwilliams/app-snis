import streamlit as st
import pandas as pd

st.set_page_config(page_title="SNIS Dashboard", layout="wide")

st.title("📊 Dashboard SNIS – Nordeste")

# =====================
# 1. Carregar os dados
# =====================
df_dados = pd.read_csv("snis_nordeste_1_filtrado.csv")
df_nat = pd.read_csv("Agregado-20251216154116.csv", encoding='latin1')

# =====================
# 2. Padronizar colunas
# (ajuste se o nome for diferente)
# =====================
# Exemplo de chave comum
chave = "CO_PRESTADOR"

# =====================
# 3. Juntar os dois CSV
# =====================
df = df_dados.merge(
    df_nat[[chave, "NATUREZA_JURIDICA"]],
    on=chave,
    how="left"
)

# =====================
# 4. Barra lateral – filtros
# =====================
st.sidebar.header("🔎 Filtros")

naturezas = st.sidebar.multiselect(
    "Natureza Jurídica",
    options=df["NATUREZA_JURIDICA"].dropna().unique()
)

if naturezas:
    df = df[df["NATUREZA_JURIDICA"].isin(naturezas)]

# =====================
# 5. Visualização
# =====================
st.subheader("📄 Dados filtrados")
st.dataframe(df)

# =====================
# 6. Análise simples
# =====================
coluna = st.selectbox(
    "Selecione um indicador:",
    df.select_dtypes(include="number").columns
)

st.write(df[coluna].describe())
