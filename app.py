import streamlit as st
import pandas as pd

st.set_page_config(page_title="SNIS Dashboard", layout="wide")

st.title("📊 Dashboard SNIS")

# Upload ou leitura do CSV
df = pd.read_csv("snis_nordeste_1_filtrado.csv")

st.subheader("📄 Visualização dos dados")
st.dataframe(df)

# Exemplo de filtro
coluna = st.selectbox("Selecione uma variável:", df.columns)

st.subheader("📈 Estatísticas")
st.write(df[coluna].describe())
