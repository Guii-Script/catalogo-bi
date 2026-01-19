import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub | BI Corporativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de variáveis de sessão
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False
if 'selected_publico' not in st.session_state:
    st.session_state.selected_publico = "Todos"

# ==============================================================================
# ESTILIZAÇÃO CSS
# ==============================================================================
def load_css():
    theme = {
        "bg_main": "#0f172a",
        "bg_card": "#1e293b",
        "border": "#334155",
        "accent": "#0ea5e9",
        "accent_glow": "rgba(14, 165, 233, 0.15)",
        "text_head": "#f1f5f9",
        "text_body": "#94a3b8",
        "success": "#10b981",
        "danger": "#ef4444"
    }

    css = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background-color: {theme['bg_main']};
            font-family: 'Inter', sans-serif;
        }}
        
        h1, h2, h3, h4 {{
            color: {theme['text_head']} !important;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        p, label, span, div {{
            color: {theme['text_body']};
        }}
        
        [data-testid="stSidebar"] {{
            background-color: {theme['bg_card']};
            border-right: 1px solid {theme['border']};
        }}
        
        .hero-container {{
            text-align: center;
            padding: 4rem 1rem;
            background: radial-gradient(circle at center, {theme['accent_glow']} 0%, transparent 70%);
            margin-bottom: 2rem;
        }}
        
        .hero-title {{
            font-size: 3rem;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }}
        
        .dashboard-card {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            padding: 0;
            transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-6px);
            border-color: {theme['accent']};
            box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.4);
        }}
        
        .card-header {{
            padding: 1.5rem;
            border-bottom: 1px solid {theme['border']};
            background-color: rgba(30, 41, 59, 0.9);
        }}
        
        .card-body {{
            padding: 1.5rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .card-footer {{
            padding: 1.2rem 1.5rem;
            background-color: rgba(15, 23, 42, 0.6);
            border-top: 1px solid {theme['border']};
        }}
        
        .tech-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            background: {theme['accent_glow']};
            color: {theme['accent']};
            border: 1px solid rgba(14, 165, 233, 0.3);
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .badge-success {{
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
            border-color: rgba(16, 185, 129, 0.3);
        }}
        
        .badge-warning {{
            background: rgba(245, 158, 11, 0.1);
            color: #f59e0b;
            border-color: rgba(245, 158, 11, 0.3);
        }}
        
        .btn-access {{
            display: block;
            width: 100%;
            text-align: center;
            background-color: {theme['accent']};
            color: white !important;
            padding: 0.8rem;
            border-radius: 8px;
            text-decoration: none !important;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
        }}
        
        .btn-access:hover {{
            background-color: #0284c7;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        }}
        
        .btn-disabled {{
            background-color: {theme['border']};
            color: {theme['text_body']} !important;
            cursor: not-allowed;
            opacity: 0.7;
        }}
        
        .btn-disabled:hover {{
            background-color: {theme['border']};
            box-shadow: none;
        }}
        
        .kpi-box {{
            background: {theme['bg_card']};
            border: 1px solid {theme['border']};
            padding: 1.8rem 1rem;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .kpi-box:hover {{
            transform: translateY(-3px);
            border-color: {theme['accent']};
        }}
        
        .kpi-val {{
            font-size: 2.2rem;
            font-weight: 700;
            color: {theme['text_head']};
            margin: 0.5rem 0;
        }}
        
        .kpi-lbl {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {theme['accent']};
            font-weight: 600;
        }}
        
        .filter-section {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .filter-title {{
            font-size: 0.9rem;
            font-weight: 600;
            color: {theme['accent']};
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .search-box {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            padding: 0.8rem 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .stats-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 0 1rem;
        }}
        
        .stat-value {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {theme['text_head']};
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            color: {theme['text_body']};
            margin-top: 0.2rem;
        }}
        
        @media (max-width: 768px) {{
            .hero-title {{
                font-size: 2rem;
            }}
            
            .dashboard-card {{
                margin-bottom: 1rem;
            }}
            
            .stats-bar {{
                flex-direction: column;
                gap: 1rem;
            }}
            
            .kpi-box {{
                margin-bottom: 1rem;
            }}
        }}
        
        .admin-login {{
            max-width: 400px;
            margin: 3rem auto;
            padding: 2rem;
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
        }}
        
        .login-title {{
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }}
        
        .access-log-table {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .table-header {{
            background-color: rgba(30, 41, 59, 0.9);
            padding: 1rem;
            border-bottom: 1px solid {theme['border']};
            font-weight: 600;
        }}
        
        .table-row {{
            padding: 1rem;
            border-bottom: 1px solid {theme['border']};
            display: flex;
            justify-content: space-between;
        }}
        
        .table-row:last-child {{
            border-bottom: none;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==============================================================================
# GERENCIAMENTO DE DADOS
# ==============================================================================
@st.cache_data(ttl=600)
def load_data():
    """Carrega dados da planilha principal."""
    try:
        url = st.secrets["GOOGLE_SHEET_URL"]
        df = pd.read_csv(url, encoding='utf-8')
        
        # Validação e tratamento de colunas
        cols_required = ['Nome_Dash', 'Descricao', 'Link', 'Status', 'Publico', 'Midia', 'Responsavel', 'Periodicidade']
        for col in cols_required:
            if col not in df.columns:
                df[col] = "N/A"
        
        df.fillna("N/A", inplace=True)
        return df.astype(str)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def generate_access_logs():
    """Gera logs de acesso simulados para demonstração."""
    dates = pd.date_range(end=datetime.now(), periods=90).tolist()
    data = []
    import random
    
    dashboards = ["Relatório de Vendas", "Análise de RH", "Dashboard Logístico", "Financeiro Consolidado", 
                  "Marketing Analytics", "Operações em Tempo Real", "Customer Success", "Supply Chain"]
    
    users = [f"user_{i:03d}" for i in range(1, 51)]
    departments = ["Vendas", "Marketing", "Financeiro", "RH", "Operações", "TI", "Diretoria"]
    
    for date in dates:
        # Variação de acessos por dia da semana
        base_access = 15 if date.weekday() < 5 else 5
        
        for _ in range(random.randint(base_access, base_access + 10)):
            data.append({
                "Data": date,
                "Dashboard": random.choice(dashboards),
                "Usuario": random.choice(users),
                "Departamento": random.choice(departments),
                "Hora": f"{random.randint(8, 19):02d}:{random.randint(0, 59):02d}"
            })
    
    df_logs = pd.DataFrame(data)
    df_logs['Data'] = pd.to_datetime(df_logs['Data'])
    return df_logs

# Carregar dados
df_full = load_data()
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else pd.DataFrame()

def get_filter_options(column):
    """Obtém opções de filtro para uma coluna específica."""
    if df_active.empty:
        return ["Todos"]
    
    options = sorted(df_active[column].unique().tolist())
    return ["Todos"] + options

# ==============================================================================
# COMPONENTES DE INTERFACE
# ==============================================================================
def render_sidebar():
    """Renderiza a barra lateral com navegação e filtros."""
    st.sidebar.markdown("### Intelligence Hub")
    
    # Ícone e título
    st.sidebar.markdown('<div style="text-align: center; margin-bottom: 2rem;">'
                       '<i class="fa-solid fa-chart-network" style="font-size: 2.5rem; color: #0ea5e9;"></i>'
                       '</div>', unsafe_allow_html=True)
    
    # Navegação
    nav_options = ["Lobby Principal", "Catálogo", "Administração"]
    nav_icons = ["fa-home", "fa-th-large", "fa-cogs"]
    
    nav = st.sidebar.radio(
        "Navegação", 
        nav_options,
        index=0 if st.session_state.page == "home" else 1 if st.session_state.page == "catalog" else 2,
        label_visibility="collapsed",
        format_func=lambda x: f" {x}"
    )
    
    # Atualizar estado da página
    if nav == "Lobby Principal":
        st.session_state.page = "home"
    elif nav == "Catálogo":
        st.session_state.page = "catalog"
    elif nav == "Administração":
        st.session_state.page = "admin"
    
    st.sidebar.markdown("---")
    
    # Filtros (apenas para catálogo)
    if st.session_state.page == "catalog":
        st.sidebar.markdown('<div class="filter-title">Filtros Avançados</div>', unsafe_allow_html=True)
        
        with st.sidebar.container():
            f_publico = st.selectbox("Público Alvo", get_filter_options("Publico"), key="filtro_publico")
            f_midia = st.selectbox("Plataforma", get_filter_options("Midia"), key="filtro_midia")
            f_resp = st.selectbox("Responsável", get_filter_options("Responsavel"), key="filtro_responsavel")
            f_periodicidade = st.selectbox("Periodicidade", get_filter_options("Periodicidade"), key="filtro_periodicidade")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown('<div style="font-size: 0.8rem; color: #64748b; text-align: center;">'
                           f'{len(df_active)} dashboards ativos'
                           '</div>', unsafe_allow_html=True)
        
        return f_publico, f_midia, f_resp, f_periodicidade
    
    return "Todos", "Todos", "Todos", "Todos"

def render_kpi_card(label, value, icon, color="#0ea5e9"):
    """Renderiza um cartão KPI."""
    return f"""
    <div class="kpi-box">
        <i class="fa-solid {icon}" style="font-size: 1.8rem; color: {color}; margin-bottom: 10px;"></i>
        <div class="kpi-val">{value}</div>
        <div class="kpi-lbl">{label}</div>
    </div>
    """

# ==============================================================================
# PÁGINAS DO SISTEMA
# ==============================================================================
def page_home():
    """Página inicial do sistema."""
    st.markdown("""
    <div class="hero-container">
        <div style="font-size: 4rem; margin-bottom: 1rem; color: #0ea5e9;">
            <i class="fa-solid fa-brain-circuit"></i>
        </div>
        <h1 class="hero-title">Hub de Inteligência Corporativa</h1>
        <p style="max-width: 600px; margin: 0 auto; font-size: 1.1rem; line-height: 1.6; color: #94a3b8;">
            Portal centralizado de dashboards e relatórios estratégicos. 
            Acesso rápido a indicadores de desempenho, análises operacionais 
            e insights para tomada de decisão.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas rápidas
    if not df_active.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_dashboards = len(df_active)
            st.markdown(render_kpi_card("Dashboards Ativos", total_dashboards, "fa-chart-line"), unsafe_allow_html=True)
        
        with col2:
            unique_platforms = df_active['Midia'].nunique()
            st.markdown(render_kpi_card("Plataformas", unique_platforms, "fa-layer-group", "#10b981"), unsafe_allow_html=True)
        
        with col3:
            unique_teams = df_active['Publico'].nunique()
            st.markdown(render_kpi_card("Times Atendidos", unique_teams, "fa-users", "#f59e0b"), unsafe_allow_html=True)
        
        with col4:
            recent_updates = len(df_active[df_active['Periodicidade'].str.contains('Diária|Semanal')])
            st.markdown(render_kpi_card("Atualizações Regulares", recent_updates, "fa-sync-alt", "#8b5cf6"), unsafe_allow_html=True)
    
    # Botão de ação principal
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Explorar Catálogo Completo", use_container_width=True, type="primary", 
                     icon="fa-search"):
            st.session_state.page = "catalog"
            st.rerun()

def page_catalog(f_pub, f_mid, f_resp, f_period):
    """Página do catálogo de dashboards."""
    st.markdown("### Catálogo de Dashboards")
    st.markdown("Explore todas as soluções de dados disponíveis por departamento, plataforma e periodicidade.")
    
    # Barra de pesquisa
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("", placeholder="Buscar por nome, descrição ou palavra-chave...", 
                              label_visibility="collapsed", key="search_input")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Limpar Filtros", use_container_width=True, type="secondary"):
            st.session_state.filtro_publico = "Todos"
            st.session_state.filtro_midia = "Todos"
            st.session_state.filtro_responsavel = "Todos"
            st.session_state.filtro_periodicidade = "Todos"
            st.rerun()
    
    # Aplicar filtros
    df_view = df_active.copy()
    
    if search:
        search_term = search.lower()
        df_view = df_view[
            df_view['Nome_Dash'].str.lower().str.contains(search_term) | 
            df_view['Descricao'].str.lower().str.contains(search_term) |
            df_view['Publico'].str.lower().str.contains(search_term)
        ]
    
    if f_pub != "Todos":
        df_view = df_view[df_view['Publico'] == f_pub]
    if f_mid != "Todos":
        df_view = df_view[df_view['Midia'] == f_mid]
    if f_resp != "Todos":
        df_view = df_view[df_view['Responsavel'] == f_resp]
    if f_period != "Todos":
        df_view = df_view[df_view['Periodicidade'] == f_period]
    
    # Mostrar estatísticas de filtro
    if not df_view.empty:
        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{len(df_view)}</div>
                <div class="stat-label">Resultados</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df_view['Midia'].nunique()}</div>
                <div class="stat-label">Plataformas</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df_view['Publico'].nunique()}</div>
                <div class="stat-label">Públicos</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{df_view['Periodicidade'].nunique()}</div>
                <div class="stat-label">Frequências</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Grid de dashboards
    if df_view.empty:
        st.info("Nenhum dashboard encontrado com os critérios atuais de filtro.")
        return
    
    # Organizar em grid responsivo
    cols_per_row = 3
    dashboard_list = df_view.to_dict('records')
    
    for i in range(0, len(dashboard_list), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = dashboard_list[i:i + cols_per_row]
        
        for idx, row in enumerate(batch):
            with cols[idx]:
                render_dashboard_card(row)

def render_dashboard_card(row):
    """Renderiza um cartão de dashboard individual."""
    # Ícone baseado na plataforma
    platform_icons = {
        'powerbi': 'fa-chart-bar',
        'tableau': 'fa-chart-pie',
        'excel': 'fa-file-excel',
        'google': 'fa-chart-line',
        'qlik': 'fa-chart-area',
        'looker': 'fa-chart-scatter'
    }
    
    midia_lower = row['Midia'].lower()
    icon = 'fa-chart-simple'
    
    for key, value in platform_icons.items():
        if key in midia_lower:
            icon = value
            break
    
    # Status e disponibilidade
    link_url = row['Link'] if row['Link'] not in ["N/A", "nan", ""] else None
    
    # Badge de periodicidade
    periodicidade = row['Periodicidade']
    freq_badge_class = "badge-success" if "Diária" in periodicidade else "badge-warning"
    
    # HTML do cartão
    card_html = f"""
    <div class="dashboard-card">
        <div class="card-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 1.1rem; line-height: 1.4;">{row['Nome_Dash']}</h4>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.3rem;">
                        <i class="fa-solid fa-user-tie"></i> {row['Responsavel']}
                    </div>
                </div>
                <i class="fa-solid {icon}" style="color: #0ea5e9; font-size: 1.5rem; margin-left: 1rem;"></i>
            </div>
        </div>
        
        <div class="card-body">
            <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 1.2rem; flex-grow: 1;">
                {row['Descricao'][:150]}{'...' if len(row['Descricao']) > 150 else ''}
            </p>
            
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: auto;">
                <span class="tech-badge">
                    <i class="fa-solid fa-display"></i> {row['Midia']}
                </span>
                <span class="tech-badge {freq_badge_class}">
                    <i class="fa-solid fa-calendar-alt"></i> {row['Periodicidade']}
                </span>
                <span class="tech-badge" style="background: rgba(168, 85, 247, 0.1); color: #a855f7;">
                    <i class="fa-solid fa-users"></i> {row['Publico']}
                </span>
            </div>
        </div>
        
        <div class="card-footer">
    """
    
    if link_url:
        card_html += f"""
            <a href="{link_url}" target="_blank" class="btn-access">
                <i class="fa-solid fa-arrow-up-right-from-square"></i> Acessar Dashboard
            </a>
        """
    else:
        card_html += """
            <button class="btn-access btn-disabled" disabled>
                <i class="fa-solid fa-clock"></i> Indisponível
            </button>
        """
    
    card_html += """
        </div>
    </div>
    <div style="margin-bottom: 1.5rem;"></div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def page_admin():
    """Página de administração (acesso restrito)."""
    
    # Sistema de login
    if not st.session_state.admin_logged:
        render_admin_login()
        return
    
    # Área administrativa (usuário autenticado)
    render_admin_dashboard()

def render_admin_login():
    """Renderiza a tela de login administrativo."""
    st.markdown("""
    <div class="admin-login">
        <div class="login-title">
            <i class="fa-solid fa-lock" style="font-size: 2rem; color: #0ea5e9; margin-bottom: 1rem;"></i>
            <h3 style="margin-bottom: 0.5rem;">Área Administrativa</h3>
            <p style="font-size: 0.9rem; color: #94a3b8;">Acesso restrito à equipe de Business Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Senha de acesso", type="password", key="admin_password")
        
        if st.button("Autenticar", use_container_width=True, type="primary", icon="fa-key"):
            try:
                if password == st.secrets["ADMIN_PASSWORD"]:
                    st.session_state.admin_logged = True
                    st.rerun()
                else:
                    st.error("Senha incorreta. Tente novamente.")
            except KeyError:
                st.error("Configuração de senha administrativa não encontrada.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_admin_dashboard():
    """Renderiza o dashboard administrativo."""
    # Cabeçalho
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Dashboard Administrativo")
        st.markdown("Monitoramento de acessos e métricas do Intelligence Hub")
    with col2:
        if st.button("Sair", use_container_width=True, type="secondary", icon="fa-sign-out-alt"):
            st.session_state.admin_logged = False
            st.rerun()
    
    st.markdown("---")
    
    # Carregar logs de acesso
    df_logs = generate_access_logs()
    
    # KPIs principais
    st.markdown("#### Métricas Principais")
    k1, k2, k3, k4 = st.columns(4)
    
    # Cálculos
    total_access = len(df_logs)
    unique_users = df_logs['Usuario'].nunique()
    top_dashboard = df_logs['Dashboard'].value_counts().idxmax()
    active_dashboards = len(df_active)
    
    # Períodos
    today = datetime.now().date()
    df_today = df_logs[df_logs['Data'].dt.date == today]
    df_week = df_logs[df_logs['Data'] >= (datetime.now() - timedelta(days=7))]
    df_month = df_logs[df_logs['Data'] >= (datetime.now() - timedelta(days=30))]
    
    with k1:
        st.markdown(render_kpi_card("Acessos Hoje", len(df_today), "fa-calendar-day", "#ef4444"), unsafe_allow_html=True)
    
    with k2:
        st.markdown(render_kpi_card("Últimos 7 Dias", len(df_week), "fa-calendar-week", "#f59e0b"), unsafe_allow_html=True)
    
    with k3:
        st.markdown(render_kpi_card("Últimos 30 Dias", len(df_month), "fa-calendar-alt", "#10b981"), unsafe_allow_html=True)
    
    with k4:
        st.markdown(render_kpi_card("Usuários Únicos", unique_users, "fa-user-check", "#8b5cf6"), unsafe_allow_html=True)
    
    # Gráficos e análises
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Análise de Acesso")
    
    tab1, tab2, tab3 = st.tabs(["Evolução Temporal", "Dashboard Popularidade", "Acessos por Departamento"])
    
    with tab1:
        # Gráfico de evolução temporal
        daily_access = df_logs.groupby(df_logs['Data'].dt.date).size().reset_index()
        daily_access.columns = ['Data', 'Acessos']
        
        chart_line = alt.Chart(daily_access).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('Data:T', title='Data'),
            y=alt.Y('Acessos:Q', title='Número de Acessos'),
            tooltip=['Data', 'Acessos']
        ).properties(height=350).configure_axis(grid=False)
        
        st.altair_chart(chart_line, use_container_width=True)
    
    with tab2:
        # Gráfico de popularidade por dashboard
        dashboard_counts = df_logs['Dashboard'].value_counts().reset_index()
        dashboard_counts.columns = ['Dashboard', 'Acessos']
        
        chart_bar = alt.Chart(dashboard_counts.head(10)).mark_bar().encode(
            x=alt.X('Acessos:Q', title='Número de Acessos'),
            y=alt.Y('Dashboard:N', sort='-x', title='Dashboard'),
            color=alt.Color('Dashboard:N', legend=None),
            tooltip=['Dashboard', 'Acessos']
        ).properties(height=400)
        
        st.altair_chart(chart_bar, use_container_width=True)
    
    with tab3:
        # Gráfico por departamento
        dept_counts = df_logs['Departamento'].value_counts().reset_index()
        dept_counts.columns = ['Departamento', 'Acessos']
        
        chart_pie = alt.Chart(dept_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Acessos", type="quantitative"),
            color=alt.Color(field="Departamento", type="nominal", legend=alt.Legend(title="Departamento")),
            tooltip=['Departamento', 'Acessos']
        ).properties(height=400, width=600)
        
        st.altair_chart(chart_pie, use_container_width=True)
    
    # Tabela de logs recentes
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Últimos Acessos")
    
    recent_logs = df_logs.sort_values('Data', ascending=False).head(10)
    
    if not recent_logs.empty:
        st.dataframe(
            recent_logs[['Data', 'Dashboard', 'Usuario', 'Departamento', 'Hora']],
            column_config={
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "Dashboard": "Dashboard",
                "Usuario": "Usuário",
                "Departamento": "Departamento",
                "Hora": "Horário"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Nenhum registro de acesso disponível.")

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================
def main():
    """Função principal de execução do aplicativo."""
    # Renderizar sidebar e obter filtros
    f_pub, f_mid, f_resp, f_period = render_sidebar()
    
    # Navegar para a página apropriada
    if st.session_state.page == "home":
        page_home()
    elif st.session_state.page == "catalog":
        page_catalog(f_pub, f_mid, f_resp, f_period)
    elif st.session_state.page == "admin":
        page_admin()
    
    # Rodapé
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 1rem;">
            <i class="fa-solid fa-shield-check"></i> Intelligence Hub v2.0 • 
            Ambiente seguro para decisões baseadas em dados
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()