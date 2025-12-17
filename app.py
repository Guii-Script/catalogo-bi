import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analytics Hub | Corporate Portfolio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PALETA DE CORES (MODERNA/SaaS) ---
COLORS = {
    "bg_main": "#F8FAFC",
    "bg_card": "#FFFFFF",
    "primary": "#0F172A",      # Slate 900
    "accent": "#4F46E5",       # Indigo 600
    "text_main": "#1E293B",    # Slate 800
    "text_muted": "#64748B",   # Slate 500
    "border": "#E2E8F0",       # Slate 200
    "success": "#10B981"
}

# --- CSS CUSTOMIZADO (CLEAN UI) ---
def load_custom_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Reset Geral */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {COLORS['bg_main']};
            font-family: 'Inter', sans-serif;
            color: {COLORS['text_main']};
        }}

        /* Header e Títulos */
        .main-title {{
            font-weight: 700;
            font-size: 2.5rem;
            color: {COLORS['primary']};
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }}
        .section-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS['primary']};
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {COLORS['border']};
        }}

        /* Cards de Dashboard */
        .db-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 1.5rem;
            height: 100%;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .db-card:hover {{
            border-color: {COLORS['accent']};
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}

        /* Tags e Status */
        .tag-container {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}
        .badge {{
            font-size: 0.75rem;
            font-weight: 500;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            background: #F1F5F9;
            color: {COLORS['text_muted']};
            border: 1px solid {COLORS['border']};
        }}
        .badge-status {{
            background: #ECFDF5;
            color: {COLORS['success']};
            border: 1px solid #D1FAE5;
        }}

        /* Botões */
        div.stButton > button {{
            background-color: {COLORS['primary']} !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
            width: 100%;
        }}
        div.stButton > button:hover {{
            background-color: {COLORS['accent']} !important;
        }}
        
        /* Ajuste Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['bg_card']};
            border-right: 1px solid {COLORS['border']};
        }}
        
        /* KPI Boxes */
        .kpi-box {{
            background: {COLORS['bg_card']};
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid {COLORS['border']};
            text-align: center;
        }}
        .kpi-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['accent']};
            display: block;
        }}
        .kpi-label {{
            font-size: 0.8rem;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
        }}
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# --- LOGICA DE DADOS ---
if 'team_selected' not in st.session_state:
    st.session_state.team_selected = False
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = "Todos"

@st.cache_data(ttl=600)
def load_data():
    try:
        url = st.secrets["GOOGLE_SHEET_URL"]
        df = pd.read_csv(url)
        df.fillna("N/A", inplace=True)
        return df
    except:
        # Fallback para exemplo estruturado se a URL falhar
        return pd.DataFrame(columns=['Nome_Dash','Descricao','Link','Status','Responsavel','Publico','Midia','Periodicidade','Horario','Divulgacao'])

df_full = load_data()
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else df_full

def get_unique_options(col):
    if df_active.empty: return ["Todos"]
    if col == "Publico":
        items = set()
        for s in df_active['Publico'].unique():
            items.update([i.strip() for i in str(s).split('/')])
        return ["Todos"] + sorted([i for i in items if i.lower() not in ["todos", "n/a"]])
    return ["Todos"] + sorted(df_active[col].unique().tolist())

# --- VIEW: SELEÇÃO INICIAL ---
if not st.session_state.team_selected:
    st.markdown("<h1 style='text-align: center; margin-top: 100px;'>Central de Business Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Selecione sua área de atuação para visualizar os painéis disponíveis.</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    teams = get_unique_options("Publico")[1:] # Remove "Todos"
    cols = st.columns(3)
    for idx, team in enumerate(teams):
        with cols[idx % 3]:
            if st.button(team, key=f"init_{team}"):
                st.session_state.team_selected = True
                st.session_state.selected_team = team
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Acessar Catálogo Completo", use_container_width=True, type="secondary"):
        st.session_state.team_selected = True
        st.session_state.selected_team = "Todos"
        st.rerun()

# --- VIEW: DASHBOARD HUB ---
else:
    # Top Bar
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"<h1 class='main-title'>Analytics Hub: {st.session_state.selected_team}</h1>", unsafe_allow_html=True)
    with c2:
        if st.button("Alterar Área"):
            st.session_state.team_selected = False
            st.rerun()

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='kpi-box'><span class='kpi-value'>{len(df_full)}</span><span class='kpi-label'>Total de Assets</span></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi-box'><span class='kpi-value'>{len(df_active)}</span><span class='kpi-label'>Painéis Ativos</span></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-box'><span class='kpi-value'>{df_active['Midia'].nunique()}</span><span class='kpi-label'>Plataformas</span></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='kpi-box'><span class='kpi-value'>10min</span><span class='kpi-label'>Refresh Rate</span></div>", unsafe_allow_html=True)

    # Filtros Laterais
    st.sidebar.title("Filtros")
    f_publico = st.sidebar.selectbox("Público-Alvo", get_unique_options("Publico"), 
                                    index=get_unique_options("Publico").index(st.session_state.selected_team) if st.session_state.selected_team in get_unique_options("Publico") else 0)
    f_midia = st.sidebar.selectbox("Plataforma", get_unique_options("Midia"))
    search = st.text_input("Buscar por nome ou tecnologia", placeholder="Ex: Financeiro, Power BI...")

    # Lógica de Filtro
    df_filtered = df_active.copy()
    if f_publico != "Todos":
        df_filtered = df_filtered[df_filtered["Publico"].str.contains(f_publico, case=False, na=False)]
    if f_midia != "Todos":
        df_filtered = df_filtered[df_filtered["Midia"] == f_midia]
    if search:
        df_filtered = df_filtered[df_filtered["Nome_Dash"].str.contains(search, case=False)]

    # Grid de Conteúdo
    if df_filtered.empty:
        st.info("Nenhum dashboard encontrado para os filtros selecionados.")
    else:
        # Agrupamento por categoria se "Todos" estiver selecionado
        groups = [("Resultados", df_filtered)] if f_publico != "Todos" else df_filtered.groupby("Publico")
        
        for name, group in groups:
            st.markdown(f"<div class='section-title'>{name}</div>", unsafe_allow_html=True)
            
            rows = [group.iloc[i:i+3] for i in range(0, len(group), 3)]
            for row_data in rows:
                cols = st.columns(3)
                for idx, (index, row) in enumerate(row_data.iterrows()):
                    with cols[idx]:
                        # Card HTML
                        st.markdown(f"""
                            <div class='db-card'>
                                <div style='font-size: 0.7rem; color: {COLORS['accent']}; font-weight: 700; text-transform: uppercase;'>{row['Midia']}</div>
                                <div style='font-size: 1.15rem; font-weight: 600; margin: 0.5rem 0;'>{row['Nome_Dash']}</div>
                                <div style='font-size: 0.85rem; color: {COLORS['text_muted']}; min-height: 50px;'>{row['Descricao']}</div>
                                <div class='tag-container'>
                                    <span class='badge badge-status'>Online</span>
                                    <span class='badge'>{row['Periodicidade']}</span>
                                </div>
                                <div style='margin-top: 1.5rem;'></div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Botões de Ação
                        btn_c1, btn_c2 = st.columns(2)
                        with btn_c1:
                            with st.popover("Metadados"):
                                st.caption("Detalhes Técnicos")
                                st.write(f"**Responsável:** {row['Responsavel']}")
                                st.write(f"**Atualização:** {row['Horario']}")
                                st.write(f"**Canal:** {row['Divulgacao']}")
                        with btn_c2:
                            link = str(row['Link']).strip()
                            if link.lower() != "n/a":
                                st.link_button("Abrir Report", link)
                            else:
                                st.button("Indisponível", disabled=True)

    st.sidebar.markdown("---")
    st.sidebar.caption("Analytics Portal v2.0.0 | Enterprise Edition")