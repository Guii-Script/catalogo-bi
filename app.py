import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Analytics Hub | Portal de Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Paleta de Cores Corporativa ---
COLORS = {
    "bg_light": "#F8FAFC",      # Branco suave (Fundo)
    "white": "#FFFFFF",         # Branco puro (Cards)
    "primary": "#0F172A",       # Azul quase preto (Títulos/Navbar)
    "secondary": "#1E293B",     # Azul Marinho Escuro (Texto Principal)
    "accent": "#3B82F6",        # Azul Royal (Destaques e Botões)
    "accent_light": "#DBEAFE",  # Azul Celeste (Badges)
    "border": "#E2E8F0",        # Cinza Azulado (Linhas e Bordas)
    "text_muted": "#64748B",    # Cinza para descrições
}

# --- CSS Profissional (Clean UI) ---
def load_custom_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Fundo da App */
        [data-testid="stAppViewContainer"] {{
            background-color: {COLORS['bg_light']};
            font-family: 'Inter', sans-serif;
        }}

        /* Header Principal */
        .main-header {{
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {COLORS['border']};
        }}

        .main-title {{
            color: {COLORS['primary']};
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }}

        /* Grid de Cards */
        .dashboard-card {{
            background-color: {COLORS['white']};
            border: 1px solid {COLORS['border']};
            padding: 1.5rem;
            border-radius: 12px;
            height: 100%;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }}
        .dashboard-card:hover {{
            border-color: {COLORS['accent']};
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }}

        /* Tipografia do Card */
        .card-category {{
            font-size: 0.75rem;
            font-weight: 700;
            color: {COLORS['accent']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS['secondary']};
            margin-bottom: 0.75rem;
        }}
        .card-desc {{
            font-size: 0.875rem;
            color: {COLORS['text_muted']};
            line-height: 1.5;
            margin-bottom: 1.25rem;
            min-height: 3rem;
        }}

        /* Badges/Tags */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            background-color: {COLORS['accent_light']};
            color: {COLORS['accent']};
            margin-right: 0.5rem;
        }}

        /* Customização dos botões nativos para o design */
        div.stButton > button {{
            background-color: {COLORS['accent']} !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            width: 100%;
        }}
        
        /* Botão Secundário (Detalhes) */
        [data-testid="stPopover"] > button {{
            background-color: transparent !important;
            color: {COLORS['text_muted']} !important;
            border: 1px solid {COLORS['border']} !important;
        }}
        
        /* KPI Boxes */
        .kpi-container {{
            background: white;
            border: 1px solid {COLORS['border']};
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
        }}
        .kpi-label {{ font-size: 0.8rem; color: {COLORS['text_muted']}; text-transform: uppercase; }}
        .kpi-value {{ font-size: 1.5rem; font-weight: 700; color: {COLORS['primary']}; }}

        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# --- Lógica de Dados (Refatorada) ---
@st.cache_data(ttl=600)
def carregar_dados_hub():
    try:
        url = st.secrets["GOOGLE_SHEET_URL"]
        df = pd.read_csv(url).fillna("N/A")
        return df.astype(str)
    except:
        st.error("Erro ao conectar à base de dados.")
        return pd.DataFrame()

df_full = carregar_dados_hub()

# Inicialização do Estado
if 'team' not in st.session_state: st.session_state.team = "Todos"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- TELA DE ENTRADA (SELEÇÃO) ---
if not st.session_state.logged_in:
    st.markdown("<div style='text-align: center; margin-top: 5rem;'>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>Hub de Inteligência de Dados</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Selecione sua unidade de negócio para continuar</p>", unsafe_allow_html=True)
    
    # Extrair times únicos do Público
    if not df_full.empty:
        publicos = set()
        for p in df_full['Publico'].unique():
            publicos.update([x.strip() for x in p.split('/') if x != 'N/A'])
        
        cols = st.columns(len(publicos) if len(publicos) < 5 else 4)
        for i, team in enumerate(sorted(list(publicos))):
            with cols[i % len(cols)]:
                if st.button(team, key=f"btn_init_{team}"):
                    st.session_state.team = team
                    st.session_state.logged_in = True
                    st.rerun()
        
        st.write("---")
        if st.button("Ver Todos os Departamentos", type="secondary", use_container_width=True):
            st.session_state.team = "Todos"
            st.session_state.logged_in = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PORTFÓLIO PRINCIPAL ---
else:
    # Sidebar
    st.sidebar.markdown(f"### Unidade: **{st.session_state.team}**")
    if st.sidebar.button("Trocar Unidade"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtros de Visão")
    search = st.sidebar.text_input("Buscar painel...", placeholder="Nome ou palavra-chave")
    f_midia = st.sidebar.selectbox("Plataforma", ["Todos"] + sorted(df_full['Midia'].unique().tolist()))

    # Filtro de Dados
    df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy()
    
    if st.session_state.team != "Todos":
        df_active = df_active[df_active['Publico'].str.contains(st.session_state.team, case=False)]
    
    if f_midia != "Todos":
        df_active = df_active[df_active['Midia'] == f_midia]
    
    if search:
        df_active = df_active[df_active['Nome_Dash'].str.contains(search, case=False) | df_active['Descricao'].str.contains(search, case=False)]

    # Header e KPIs
    st.markdown(f"<h1 class='main-title'>Analytics Hub</h1>", unsafe_allow_html=True)
    
    k1, k2, k3 = st.columns(3)
    with k1: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Painéis Ativos</div><div class='kpi-value'>{len(df_active)}</div></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Atualização Médio</div><div class='kpi-value'>Diária</div></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='kpi-container'><div class='kpi-label'>Unidade</div><div class='kpi-value'>{st.session_state.team}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Grid de Dashboards
    if df_active.empty:
        st.info("Nenhum dashboard localizado para os critérios aplicados.")
    else:
        # Loop para criar as linhas
        dash_list = df_active.to_dict('records')
        for i in range(0, len(dash_list), 3):
            cols = st.columns(3)
            chunk = dash_list[i:i+3]
            
            for j, row in enumerate(chunk):
                with cols[j]:
                    # Card HTML
                    st.markdown(f"""
                        <div class='dashboard-card'>
                            <div class='card-category'>{row['Midia']}</div>
                            <div class='card-title'>{row['Nome_Dash']}</div>
                            <div class='card-desc'>{row['Descricao']}</div>
                            <div style='margin-bottom: 1.5rem;'>
                                <span class='badge'>{row['Periodicidade']}</span>
                                <span class='badge'>{row['Responsavel'].split()[0]}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Ações do Card (Abaixo do HTML para manter funcionalidade Streamlit)
                    c_btn1, c_btn2 = st.columns([1, 1.2])
                    with c_btn1:
                        with st.popover("Metadados"):
                            st.caption("Informações Adicionais")
                            st.write(f"**Público:** {row['Publico']}")
                            st.write(f"**Horário:** {row['Horario']}")
                            st.write(f"**Divulgação:** {row['Divulgacao']}")
                    with c_btn2:
                        link = row['Link'].strip()
                        if link.lower() != "n/a":
                            st.link_button("Acessar Painel", link)
                        else:
                            st.button("Em breve", disabled=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.caption("v3.0 • Enterprise Dashboard Manager")