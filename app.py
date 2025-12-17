import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard SNIS – Nordeste", layout="wide")

st.title("📊 Dashboard SNIS – Nordeste")

st.markdown("""
Este dashboard utiliza dados do **SNIS**, respeitando os diferentes níveis de agregação:
- **Dados municipais** para análise territorial e temporal;
- **Dados agregados por prestador** para análise institucional (Natureza Jurídica).
""")

# =====================
# Leitura dos dados
# =====================

# Dados municipais
df_mun = pd.read_csv(
    "snis_nordeste_1_filtrado.csv",
    sep=",",
    encoding="utf-8"
)

# Dados por prestador (natureza jurídica)
df_prest = pd.read_csv(
    "Agregado-20251216154116.csv",
    sep=";",
    encoding="latin1"
)

# =====================
# SIDEBAR
# =====================
st.sidebar.header("🔎 Filtros")

# Filtro de ano (municipal)
anos = sorted(df_mun["ano"].dropna().unique())
ano_sel = st.sidebar.selectbox("Ano", anos)

df_mun_f = df_mun[df_mun["ano"] == ano_sel]

# Filtro de UF
ufs = sorted(df_mun_f["sigla_uf"].dropna().unique())
ufs_sel = st.sidebar.multiselect("UF", ufs, default=ufs)

df_mun_f = df_mun_f[df_mun_f["sigla_uf"].isin(ufs_sel)]

# Filtro natureza jurídica (AGREGADO)
col_nat = "natureza_juridica"

if col_nat in df_prest.columns:
    naturezas = st.sidebar.multiselect(
        "Natureza Jurídica (prestadores)",
        sorted(df_prest[col_nat].dropna().unique())
    )

    if naturezas:
        df_prest = df_prest[df_prest[col_nat].isin(naturezas)]

# =====================
# VISUALIZAÇÃO MUNICIPAL
# =====================
st.subheader("📍 Indicadores Municipais")

colunas_numericas = df_mun_f.select_dtypes(include="number").columns.tolist()

indicador = st.selectbox(
    "Selecione um indicador municipal:",
    colunas_numericas
)

st.metric(
    label=f"Média – {indicador}",
    value=f"{df_mun_f[indicador].mean():,.2f}"
)

st.dataframe(
    df_mun_f[["sigla_uf", "id_municipio", indicador]]
)

# =====================
# VISUALIZAÇÃO INSTITUCIONAL
# =====================
st.subheader("🏛️ Análise por Natureza Jurídica (Agregado)")

colunas_num_prest = df_prest.select_dtypes(include="number").columns.tolist()

indicador_prest = st.selectbox(
    "Selecione um indicador institucional:",
    colunas_num_prest
)

st.dataframe(
    df_prest[[col_nat, indicador_prest]]
    .groupby(col_nat)
    .mean()
    .reset_index()
)
