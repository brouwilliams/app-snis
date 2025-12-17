import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard SNIS – Diagnóstico", layout="wide")

st.title("🔎 Diagnóstico dos arquivos SNIS")

st.write("Este app serve apenas para identificar as colunas corretas dos CSV.")

# =====================
# Carregar os CSV
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
# Mostrar colunas
# =====================
st.subheader("📄 Colunas – snis_nordeste_1_filtrado.csv")
st.write(df_dados.columns.tolist())

st.subheader("📄 Colunas – Agregado-20251216154116.csv")
st.write(df_nat.columns.tolist())

st.success("Se você está vendo as listas acima, os arquivos foram lidos corretamente.")
