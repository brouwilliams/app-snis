import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard SNIS – Nordeste", layout="wide")

st.title("📊 Dashboard SNIS – Nordeste")

# =====================
# Leitura CORRETA dos CSV
# =====================

# CSV 1 – usa vírgula
df_dados = pd.read_csv(
    "snis_nordeste_1_filtrado.csv",
    sep=",",
    encoding="utf-8"
)

# CSV 2 – usa ponto e vírgula
df_nat = pd.read_csv(
    "Agregado-20251216154116.csv",
    sep=";",
    encoding="latin1"
)

# =====================
# Mostrar colunas (checagem final)
# =====================
with st.expander("🔎 Ver colunas dos arquivos"):
    st.write("Colunas – dados principais:")
    st.write(df_dados.columns.tolist())

    st.write("Colunas – natureza jurídica:")
    st.write(df_nat.columns.tolist())

st.success("Arquivos carregados corretamente.")
