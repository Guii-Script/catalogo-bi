import streamlit as st
import pandas as pd
from utils import carregar_dados, lista
from ui_components import (
    load_css, 
    render_team_selector, 
    render_header_stats, 
    render_sidebar, 
    render_dashboard_grid
)

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Carregar CSS Customizado ---
load_css()

# --- Inicialização do Session State ---
if 'team_selected' not in st.session_state:
    st.session_state.team_selected = False
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = "Todos"

# --- Carregamento de Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado.")
    st.stop()

# Carrega o DataFrame COMPLETO para os KPIs
df_full = carregar_dados(URL_PLANILHA)

# Cria um DataFrame filtrado (só ativos) para usar no app
if not df_full.empty and 'Status' in df_full.columns:
    df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy()
else:
    df_active = pd.DataFrame(columns=df_full.columns)


# --- Roteador Principal (Controla qual tela exibir) ---
if not st.session_state.team_selected:
    # Tela 1: Seleção de Time
    render_team_selector(df_active, lista)

else:
    # Tela 2: Galeria Principal de Dashboards
    
    # 1. Renderiza o Header e os KPIs (usando df_full)
    render_header_stats(df_full)
    
    # 2. Renderiza a Sidebar e obtém os valores dos filtros (usando df_active)
    filtro_publico, filtro_responsavel, filtro_midia = render_sidebar(df_active, lista)
    
    # 3. Lógica de Busca e Filtro (permanece no app principal)
    search_term = st.text_input("🔍 **Buscar dashboards:**", placeholder="Digite o nome do dashboard, tecnologia ou palavra-chave...")
    st.markdown("<br>", unsafe_allow_html=True) 

    # Começa a filtragem a partir dos dashboards ativos
    df_filtrado = df_active.copy()
    
    if search_term:
        df_filtrado = df_filtrado[
            df_filtrado["Nome_Dash"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descricao"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Midia"].str.contains(search_term, case=False, na=False)
        ]
    
    filter_mapping = {
        "Responsavel": (filtro_responsavel, "Todos"),
        "Publico": (filtro_publico, "Todos"),
        "Midia": (filtro_midia, "Todos")
    }
    
    for col, (filtro, padrao) in filter_mapping.items():
        if filtro != padrao:
            df_filtrado = df_filtrado[df_filtrado[col] == filtro]

    # 4. Renderiza o Grid de Dashboards
    render_dashboard_grid(df_filtrado, filtro_publico)