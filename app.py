import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard SNIS – Nordeste", layout="wide")

st.title("📊 Dashboard SNIS – Nordeste")

# =====================
# Leitura dos dados
# =====================
df_dados = pd.read_csv(
    "snis_nordeste_1_filtrado.csv",
    sep=";",
    encoding="latin1"
)

df_nat = pd.read_csv(
    "Agregado-20251216154116.csv",
    sep=";",
    encoding="latin1"
)

# =====================
# Ajuste da chave (CONFIRA O NOME)
# =====================
chave = "CO_PRESTADOR"

# =====================
# Merge
# =====================
df = df_dados.merge(
    df_nat[[chave, "NATUREZA_JURIDICA"]],
    on=chave,
    how="left"
)

# =====================
# Filtros
# =====================
st.sidebar.header("🔎 Filtros")

naturezas = st.sidebar.multiselect(
    "Natureza Jurídica",
    sorted(df["NATUREZA_JURIDICA"].dropna().unique())
)

if naturezas:
    df = df[df["NATUREZA_JURIDICA"].isin(naturezas)]

# =====================
# Visualização
# =====================
st.subheader("📄 Dados filtrados")
st.dataframe(df)

coluna = st.selectbox(
    "Selecione um indicador:",
    df.select_dtypes(include="number").columns
)

st.subheader("📈 Estatísticas descritivas")
st.write(df[coluna].describe())
