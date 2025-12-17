import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SNIS – Nordeste", layout="wide")

st.title("📊 Saneamento Básico – Nordeste (SNIS)")

st.markdown("""
Este aplicativo apresenta indicadores do **SNIS** para a região Nordeste,  
com filtros por **ano**, **UF** e **natureza jurídica dos prestadores**.
""")

# =====================
# LEITURA DOS DADOS
# =====================

df_mun = pd.read_csv(
    "snis_nordeste_1_filtrado.csv",
    sep=",",
    encoding="utf-8"
)

df_nat = pd.read_csv(
    "Agregado-20251216154116.csv",
    sep=";",
    encoding="latin1"
)

# =====================
# LIMPEZA BÁSICA
# =====================

# Remove colunas Unnamed
df_nat = df_nat.loc[:, ~df_nat.columns.str.contains("^Unnamed")]

# Padroniza nomes
df_nat.columns = [c.strip().lower() for c in df_nat.columns]

# Nome correto da natureza jurídica
col_nat = "natureza_juridica"

# =====================
# SIDEBAR – FILTROS
# =====================

st.sidebar.header("🔎 Filtros")

# Ano
anos = sorted(df_mun["ano"].dropna().unique())
ano_sel = st.sidebar.selectbox("Ano", anos)

# UF
ufs = sorted(df_mun["sigla_uf"].dropna().unique())
uf_sel = st.sidebar.multiselect("UF", ufs, default=ufs)

df_mun_f = df_mun[
    (df_mun["ano"] == ano_sel) &
    (df_mun["sigla_uf"].isin(uf_sel))
]

# Natureza Jurídica
if col_nat in df_nat.columns:
    naturezas = sorted(df_nat[col_nat].dropna().unique())
    nat_sel = st.sidebar.multiselect(
        "Natureza Jurídica (Prestadores)",
        naturezas
    )
    if nat_sel:
        df_nat = df_nat[df_nat[col_nat].isin(nat_sel)]

# =====================
# INDICADORES MUNICIPAIS
# =====================

st.subheader("📍 Indicadores Municipais")

num_cols_mun = df_mun_f.select_dtypes(include="number").columns.tolist()

indicador_mun = st.selectbox(
    "Indicador municipal:",
    num_cols_mun
)

st.metric(
    "Média",
    f"{df_mun_f[indicador_mun].mean():,.2f}"
)

st.dataframe(
    df_mun_f[["sigla_uf", "id_municipio", indicador_mun]]
)

# =====================
# GRÁFICO MUNICIPAL
# =====================

fig, ax = plt.subplots()
df_mun_f.groupby("sigla_uf")[indicador_mun].mean().plot(kind="bar", ax=ax)
ax.set_ylabel(indicador_mun)
ax.set_title("Média por UF")
st.pyplot(fig)

# =====================
# ANÁLISE INSTITUCIONAL
# =====================

st.subheader("🏛️ Análise por Natureza Jurídica")

num_cols_nat = df_nat.select_dtypes(include="number").columns.tolist()

if len(num_cols_nat) == 0:
    st.warning("Não há indicadores numéricos no arquivo agregado.")
else:
    indicador_nat = st.selectbox(
        "Indicador institucional:",
        num_cols_nat
    )

    tabela_nat = (
        df_nat
        .groupby(col_nat)[indicador_nat]
        .mean()
        .reset_index()
        .sort_values(indicador_nat, ascending=False)
    )

    st.dataframe(tabela_nat)

    fig2, ax2 = plt.subplots()
    ax2.barh(tabela_nat[col_nat], tabela_nat[indicador_nat])
    ax2.set_xlabel(indicador_nat)
    ax2.set_title("Média por Natureza Jurídica")
    st.pyplot(fig2)
