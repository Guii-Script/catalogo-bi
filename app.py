import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Catálogo de Dashboards de BI",
    page_icon="📊",
    layout="wide"
)


# Cole aqui o link CSV que você copiou do Google Sheets
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS43tcOACO6MB_fDbMeuv4j3bItCp9FrwCVb5lZK3udIiOV9YQARp7rUR1jXqWl5QV3wmg__esSMcpV/pub?gid=0&single=true&output=csv"

# --- Título ---
st.title("📊 Catálogo Centralizado de Dashboards de BI")
st.write("Use a busca e os filtros para encontrar o dashboard que você precisa.")

# --- Cache ---
# O Streamlit guarda os dados por 10 minutos (600 segundos) para não
# sobrecarregar a planilha. Após 10 min, ele busca os dados novos.
@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return pd.DataFrame() # Retorna um dataframe vazio em caso de erro

# --- Carregar e Filtrar ---
df = carregar_dados(URL_PLANILHA)

if not df.empty:
    st.sidebar.header("Filtros")
    
    # Filtro por Departamento
    departamentos = ["Todos"] + sorted(list(df['Departamento'].unique()))
    filtro_depto = st.sidebar.selectbox("Filtrar por Departamento:", departamentos)

    if filtro_depto == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df['Departamento'] == filtro_depto]

    # --- Exibir os Dashboards ---
    st.dataframe(df_filtrado)
else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha.")

st.sidebar.info("Para adicionar ou corrigir um dashboard, basta editar a planilha Google associada.")