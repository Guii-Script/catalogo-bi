import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Catálogo de Dashboards de BI",
    page_icon="📊",
    layout="wide"  # "wide" é essencial para tabelas com muitas colunas
)

# --- O LINK MÁGICO ---
# Cole aqui o link CSV que você copiou do Google Sheets
# (Arquivo > Compartilhar > Publicar na web > .csv)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS43tcOACO6MB_fDbMeuv4j3bItCp9FrwCVb5lZK3udIiOV9YQARp7rUR1jXqWl5QV3wmg__esSMcpV/pub?gid=0&single=true&output=csv"

# --- Título ---
st.title("📊 Catálogo Centralizado de Dashboards de BI")
st.write("Use os filtros na barra lateral para encontrar o dashboard que você precisa.")

# --- Cache ---
# O Streamlit guarda os dados por 10 minutos (600 segundos)
# Depois disso, ele busca os dados novos da planilha.
@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        # Lê o CSV. O encoding 'utf-8' ajuda com acentos (ex: Descrição)
        df = pd.read_csv(url, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        st.info("Verifique se o link da planilha está correto e se ela está publicada como CSV.")
        return pd.DataFrame() # Retorna um dataframe vazio em caso de erro

# --- Carregar Dados ---
df = carregar_dados(URL_PLANILHA)

if not df.empty:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header("Filtros do Catálogo")

    # Criar listas de opções para os filtros, incluindo "Todos"
    # O .dropna() remove valores vazios que podem virar opções de filtro
    
    # Filtro por Divisão
    divisoes = ["Todos"] + sorted(list(df['Divisão'].dropna().unique()))
    filtro_divisao = st.sidebar.selectbox("Filtrar por Divisão:", divisoes)
    
    # Filtro por Responsável
    responsaveis = ["Todos"] + sorted(list(df['Responsável'].dropna().unique()))
    filtro_responsavel = st.sidebar.selectbox("Filtrar por Responsável:", responsaveis)

    # Filtro por Status (Ex: Ativo/Inativo)
    status_opcoes = ["Todos"] + sorted(list(df['Status'].dropna().unique()))
    filtro_status = st.sidebar.selectbox("Filtrar por Status:", status_opcoes)
    
    # --- Lógica de Filtragem ---
    
    # Começa com o dataframe completo
    df_filtrado = df

    if filtro_divisao != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Divisão'] == filtro_divisao]
    
    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    
    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    # --- Exibir a Tabela ---
    st.write(f"Exibindo {len(df_filtrado)} dashboards:")
    
    # st.dataframe é ideal para tabelas grandes
    st.dataframe(
        df_filtrado,
        # Esta configuração detecta uma coluna chamada "Link"
        # e a transforma em um link clicável.
        column_config={
            "Link": st.column_config.LinkColumn(
                "Link de Acesso", # Texto que aparece no cabeçalho da coluna
                display_text="Acessar Dashboard" # Texto que aparece em cada link
            )
        },
        use_container_width=True # Faz a tabela usar a largura inteira
    )

else:
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos a partir da planilha principal.")