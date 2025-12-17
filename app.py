import streamlit as st
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Inicialização do Session State ---
if 'team_selected' not in st.session_state:
    st.session_state.team_selected = False
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = "Todos"

# --- Paleta de Cores e Configurações de Design ---
THEME = {
    "bg_dark": "#0f172a",          # Slate 900
    "bg_card": "rgba(30, 41, 59, 0.7)", # Slate 800 (Glass)
    "border": "rgba(148, 163, 184, 0.1)",
    "accent": "#38bdf8",           # Sky 400
    "accent_hover": "#0ea5e9",     # Sky 500
    "text_main": "#f8fafc",        # Slate 50
    "text_muted": "#94a3b8",       # Slate 400
    "success": "#10b981",          # Emerald 500
    "offline": "#64748b",          # Slate 500
}

# --- CSS Profissional (Método Seguro) ---
def load_custom_css():
    # Definimos o CSS como string pura para evitar conflitos de formatação do Python
    raw_css = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background-color: VAR_BG_DARK;
            font-family: 'Inter', sans-serif;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        /* HEADER */
        .header-container {
            text-align: center;
            margin-bottom: 4rem;
            padding: 3rem 1rem;
            background: radial-gradient(circle at center, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
        }
        
        .header-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -0.05em;
        }
        
        .header-subtitle {
            color: VAR_TEXT_MUTED;
            font-size: 1.1rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }

        /* KPIS */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .kpi-card {
            background: VAR_BG_CARD;
            border: 1px solid VAR_BORDER;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            transition: transform 0.2s ease;
        }
        .kpi-card:hover { transform: translateY(-2px); border-color: VAR_ACCENT; }
        
        .kpi-value { font-size: 2rem; font-weight: 700; color: VAR_TEXT_MAIN; }
        .kpi-label { color: VAR_ACCENT; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-top: 5px; }
        .kpi-icon { font-size: 1.5rem; color: VAR_TEXT_MUTED; margin-bottom: 10px; opacity: 0.5; }

        /* INPUTS */
        [data-testid="stTextInput"] input, [data-testid="stSelectbox"] > div > div {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid VAR_BORDER !important;
            border-radius: 8px !important;
        }
        [data-testid="stTextInput"] input:focus { border-color: VAR_ACCENT !important; }

        /* CARDS */
        .dash-card-header {
            background: VAR_BG_CARD;
            border: 1px solid VAR_BORDER;
            border-bottom: none;
            border-radius: 12px 12px 0 0;
            padding: 0;
            overflow: hidden;
            position: relative;
        }
        
        .dash-img-container {
            width: 100%;
            height: 160px;
            overflow: hidden;
            position: relative;
        }
        
        .dash-img-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        
        .dash-card-header:hover .dash-img-container img { transform: scale(1.05); }
        
        .dash-content {
            padding: 1.25rem;
        }
        
        .dash-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: VAR_TEXT_MAIN;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .dash-desc {
            font-size: 0.85rem;
            color: VAR_TEXT_MUTED;
            line-height: 1.5;
            height: 40px; 
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin-bottom: 1rem;
        }
        
        /* TAGS */
        .meta-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.5rem; }
        .badge {
            font-size: 0.7rem;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .badge-tech { background: rgba(56, 189, 248, 0.1); color: VAR_ACCENT; border: 1px solid rgba(56, 189, 248, 0.2); }
        .badge-status-on { background: rgba(16, 185, 129, 0.1); color: VAR_SUCCESS; border: 1px solid rgba(16, 185, 129, 0.2); }
        .badge-status-off { background: rgba(100, 116, 139, 0.1); color: VAR_OFFLINE; border: 1px solid rgba(100, 116, 139, 0.2); }

        /* BOTOES */
        div[data-testid="column"] button {
            width: 100%;
            border-radius: 0 0 12px 12px !important;
            border: 1px solid VAR_BORDER !important;
            background-color: #1e293b !important;
            color: white !important;
            font-weight: 500 !important;
            transition: all 0.3s !important;
        }
        
        div[data-testid="column"] button:hover {
            border-color: VAR_ACCENT !important;
            color: VAR_ACCENT !important;
            background-color: rgba(56, 189, 248, 0.05) !important;
        }

        div[data-testid="column"] a {
            text-decoration: none;
        }
        
        [data-testid="stLinkButton"] > a {
            background: linear-gradient(135deg, VAR_ACCENT, #2563eb) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
        }
        [data-testid="stLinkButton"] > a:hover {
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
            transform: translateY(-2px) !important;
        }

        hr { border-color: VAR_BORDER; margin: 3rem 0; }
        </style>
    """
    
    # Substituição Segura das Variáveis
    final_css = raw_css.replace("VAR_BG_DARK", THEME['bg_dark']) \
                       .replace("VAR_BG_CARD", THEME['bg_card']) \
                       .replace("VAR_BORDER", THEME['border']) \
                       .replace("VAR_ACCENT", THEME['accent']) \
                       .replace("VAR_TEXT_MAIN", THEME['text_main']) \
                       .replace("VAR_TEXT_MUTED", THEME['text_muted']) \
                       .replace("VAR_SUCCESS", THEME['success']) \
                       .replace("VAR_OFFLINE", THEME['offline'])
    
    st.markdown(final_css, unsafe_allow_html=True)

# Executa o CSS
load_custom_css()

# --- Carregamento de Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("⚠️ Configuração ausente: 'GOOGLE_SHEET_URL' não encontrado nos secrets.")
    st.stop()

@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_esperadas = ['Nome_Dash','Descricao', 'Imagem_Path','Link','Status','Responsavel','Publico','Midia','Periodicidade','Horario','Divulgacao']
        for c in colunas_esperadas:
            if c not in df.columns: df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao conectar com a base de dados: {e}")
        return pd.DataFrame()

# Carrega Dados
df_full = carregar_dados(URL_PLANILHA)
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else pd.DataFrame(columns=df_full.columns)

# --- Função Helper ---
def get_unique_list(col):
    if df_active.empty: return ["Todos"]
    if col == "Publico":
        raw_list = df_active['Publico'].replace('N/A', pd.NA).dropna().unique()
        split_set = set()
        for item in raw_list:
            parts = [p.strip() for p in item.split('/')]
            split_set.update(parts)
        final_list = sorted(list(split_set))
        return ["Todos"] + [x for x in final_list if x.lower() not in ["todos", "n/a", ""]]
    return ["Todos"] + sorted(df_active[col].replace('N/A', pd.NA).dropna().unique().tolist())

# ==============================================================================
# TELA 1: SELEÇÃO DE SETOR (LANDING PAGE)
# ==============================================================================
if not st.session_state.team_selected:
    
    st.markdown("""
        <div class="header-container" style="margin-top: 5vh;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🚀</div>
            <h1 class="header-title">Bem-vindo ao BI Hub</h1>
            <p class="header-subtitle">Central de inteligência e análise de dados corporativos.<br>Selecione seu setor para acessar os indicadores estratégicos.</p>
        </div>
    """, unsafe_allow_html=True)

    if not df_active.empty:
        teams = get_unique_list("Publico")
        teams = [t for t in teams if t != "Todos"]

        if not teams:
            st.warning("Nenhum setor público identificado. Carregando visão geral.")
            if st.button("Acessar Sistema"):
                st.session_state.team_selected = True
                st.session_state.selected_team = "Todos"
                st.rerun()
        else:
            st.markdown(f"<h3 style='text-align:center; color:{THEME['text_muted']}; margin-bottom:2rem; font-weight:400;'>Selecione sua área de atuação</h3>", unsafe_allow_html=True)
            
            # Grid de botões estilizados
            col_count = 4
            cols = st.columns(col_count)
            for idx, team in enumerate(teams):
                with cols[idx % col_count]:
                    if st.button(f"{team}", key=f"land_{team}", use_container_width=True):
                        st.session_state.team_selected = True
                        st.session_state.selected_team = team
                        st.rerun()

            st.markdown("<br><br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1,2,1])
            with c2:
                if st.button("Ver Catálogo Completo ➜", use_container_width=True):
                    st.session_state.team_selected = True
                    st.session_state.selected_team = "Todos"
                    st.rerun()
    else:
        st.info("Inicializando sistema e carregando dados...")

# ==============================================================================
# TELA 2: DASHBOARD GALLERY (MAIN APP)
# ==============================================================================
else:
    # --- Sidebar ---
    st.sidebar.markdown(f"<h2 style='color:{THEME['text_main']}; font-weight:800;'>BI <span style='color:{THEME['accent']}'>Hub</span></h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    if st.sidebar.button("↩ Voltar ao Menu", use_container_width=True):
        st.session_state.team_selected = False
        st.session_state.selected_team = "Todos"
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.caption("FILTROS GLOBAIS")

    # Filtros
    if not df_active.empty:
        publico_opts = get_unique_list("Publico")
        # Tenta preservar a seleção caso o usuário mude
        current_selection = st.session_state.selected_team
        idx_pub = publico_opts.index(current_selection) if current_selection in publico_opts else 0
        
        sel_publico = st.sidebar.selectbox("🎯 Público Alvo", publico_opts, index=idx_pub)
        sel_resp = st.sidebar.selectbox("👤 Responsável", get_unique_list("Responsavel"))
        sel_midia = st.sidebar.selectbox("💻 Plataforma", get_unique_list("Midia"))
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Status:** Conectado\n\n**Atualizado:** {pd.Timestamp.now().strftime('%H:%M')}")

    # --- Header Principal ---
    # Calculando estatísticas básicas
    total_active = len(df_active)
    
    st.markdown(f"""
        <div class="header-container" style="padding: 1rem 0; margin-bottom: 2rem; text-align: left;">
            <h1 class="header-title" style="font-size: 2.5rem;">Catálogo de Dashboards</h1>
            <p class="header-subtitle" style="margin: 0; text-align: left;">
                Visão consolidada dos indicadores de performance
                <span style="color: {THEME['accent']}"> | {sel_publico}</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- KPIs ---
    col1, col2, col3, col4 = st.columns(4)
    kpi_data = [
        ("Total Disponível", len(df_full), "fa-layer-group"),
        ("Dashboards Ativos", len(df_active), "fa-chart-line"),
        ("Setores Atendidos", df_active['Publico'].nunique(), "fa-users"),
        ("Plataformas", df_active['Midia'].nunique(), "fa-server")
    ]
    
    for col, (label, val, icon) in zip([col1, col2, col3, col4], kpi_data):
        with col:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fa-solid {icon}"></i></div>
                    <div class="kpi-value">{val}</div>
                    <div class="kpi-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    # --- Barra de Busca ---
    st.markdown("<br>", unsafe_allow_html=True)
    search_term = st.text_input("", placeholder="🔍 Busque por nome do relatório, KPI ou tecnologia...", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Filtragem de Dados ---
    if df_active.empty:
        st.warning("Base de dados vazia ou inativa.")
    else:
        df_show = df_active.copy()
        
        # Filtro Texto
        if search_term:
            t = search_term.lower()
            df_show = df_show[
                df_show["Nome_Dash"].str.lower().str.contains(t) |
                df_show["Descricao"].str.lower().str.contains(t) |
                df_show["Midia"].str.lower().str.contains(t)
            ]
        
        # Filtros Sidebar
        if sel_resp != "Todos": df_show = df_show[df_show["Responsavel"] == sel_resp]
        if sel_midia != "Todos": df_show = df_show[df_show["Midia"] == sel_midia]
        if sel_publico != "Todos": df_show = df_show[df_show["Publico"].str.contains(sel_publico, case=False, na=False)]

        # --- Renderização dos Cards ---
        if df_show.empty:
            st.markdown(f"""
                <div style="text-align: center; padding: 4rem; color: {THEME['offline']};">
                    <i class="fa-regular fa-folder-open" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                    <h3>Nenhum dashboard encontrado</h3>
                    <p>Tente ajustar os filtros ou o termo de busca.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Agrupamento Lógico
            if sel_publico != "Todos":
                groups = [("Resultados Filtrados", df_show)]
            else:
                unique_groups = sorted(df_show["Publico"].replace('N/A', pd.NA).dropna().unique())
                groups = []
                for g in unique_groups:
                    subset = df_show[df_show["Publico"] == g]
                    if not subset.empty: groups.append((g, subset))

            # Loop de Exibição
            for group_name, subset in groups:
                if group_name != "Resultados Filtrados":
                    st.markdown(f"<h3 style='margin-top:2rem; margin-bottom:1rem; border-left: 4px solid {THEME['accent']}; padding-left: 10px; color: white;'>{group_name}</h3>", unsafe_allow_html=True)
                
                rows = subset.to_dict('records')
                N_COLS = 3
                
                for i in range(0, len(rows), N_COLS):
                    cols = st.columns(N_COLS)
                    batch = rows[i:i+N_COLS]
                    
                    for j, row in enumerate(batch):
                        with cols[j]:
                            # Ícone dinâmico baseado na mídia
                            midia_lower = str(row['Midia']).lower()
                            icon_class = "fa-chart-simple"
                            if "power" in midia_lower: icon_class = "fa-chart-bar"
                            elif "excel" in midia_lower: icon_class = "fa-file-excel"
                            elif "google" in midia_lower: icon_class = "fa-google"
                            
                            status_badge = "badge-status-on" if str(row['Status']).lower() == 'ativo' else "badge-status-off"
                            
                            # --- 1. Parte Visual (HTML) ---
                            st.markdown(f"""
                            <div class="dash-card-header">
                                <div class="dash-img-container">
                                    <img src="{row.get('Imagem_Path', 'https://via.placeholder.com/400x200?text=Analytics')}" onerror="this.src='https://via.placeholder.com/400x200?text=No+Image'">
                                </div>
                                <div class="dash-content">
                                    <div class="dash-title"><i class="fa-solid {icon_class}" style="color: {THEME['accent']}"></i> {row['Nome_Dash']}</div>
                                    <div class="dash-desc" title="{row['Descricao']}">{row['Descricao']}</div>
                                    <div class="meta-tags">
                                        <span class="badge badge-tech">{row['Midia']}</span>
                                        <span class="badge {status_badge}">{row['Status']}</span>
                                        <span class="badge badge-tech"><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # --- 2. Parte Interativa (Botões) ---
                            b_col1, b_col2 = st.columns([1, 1])
                            with b_col1:
                                with st.popover("📋 Detalhes", use_container_width=True):
                                    st.markdown(f"""
                                    ### Ficha Técnica
                                    - **Responsável:** {row['Responsavel']}
                                    - **Atualização:** {row['Periodicidade']}
                                    - **Horário:** {row['Horario']}
                                    - **Público:** {row['Publico']}
                                    - **Forma de Divulgação:** {row['Divulgacao']}
                                    """)
                            
                            with b_col2:
                                link = row.get('Link', '#')
                                if link and str(link).lower() not in ['nan', 'n/a', '']:
                                    st.link_button("Acessar 🚀", link, use_container_width=True)
                                else:
                                    st.button("Indisponível", disabled=True, key=f"btn_dis_{i}_{j}", use_container_width=True)
                            
                            # Espaçamento inferior
                            st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)