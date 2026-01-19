import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import random

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
    }

    css = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            background-color: {theme['bg_main']};
            font-family: 'Inter', sans-serif;
        }}
        
        h1, h2, h3, h4 {{
            color: {theme['text_head']} !important;
            font-weight: 600;
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
        }}
        
        /* Cards */
        .dashboard-card {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            height: 100%;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
            overflow: hidden;
        }}
        
        .dashboard-card:hover {{
            transform: translateY(-4px);
            border-color: {theme['accent']};
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }}
        
        .card-header {{
            padding: 1.25rem;
            border-bottom: 1px solid {theme['border']};
            background-color: rgba(30, 41, 59, 0.5);
        }}
        
        .card-body {{
            padding: 1.25rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .card-footer {{
            padding: 1rem 1.25rem;
            background-color: rgba(15, 23, 42, 0.3);
            border-top: 1px solid {theme['border']};
        }}
        
        /* Badges */
        .tech-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 600;
            background: {theme['accent_glow']};
            color: {theme['accent']};
            border: 1px solid rgba(14, 165, 233, 0.3);
        }}
        
        .badge-success {{ background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.3); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.1); color: #f59e0b; border-color: rgba(245, 158, 11, 0.3); }}
        
        /* Buttons */
        .btn-access {{
            display: block;
            width: 100%;
            text-align: center;
            background-color: {theme['accent']};
            color: white !important;
            padding: 0.75rem;
            border-radius: 6px;
            text-decoration: none !important;
            font-weight: 500;
            transition: background-color 0.2s;
            border: none;
        }}
        
        .btn-access:hover {{ background-color: #0284c7; }}
        
        .btn-disabled {{
            background-color: {theme['border']};
            cursor: not-allowed;
            opacity: 0.6;
        }}

        /* KPI Box */
        .kpi-box {{
            background: {theme['bg_card']};
            border: 1px solid {theme['border']};
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .kpi-val {{ font-size: 2rem; font-weight: 700; color: {theme['text_head']}; }}
        .kpi-lbl {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.5rem; }}
        
        /* Admin */
        .admin-login {{
            max-width: 400px;
            margin: 4rem auto;
            padding: 2rem;
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==============================================================================
# GERENCIAMENTO DE DADOS
# ==============================================================================
def get_mock_data():
    """Gera dados fictícios caso não haja conexão com Google Sheets."""
    data = {
        'Nome_Dash': ['Vendas Global', 'RH Analytics', 'Logística Real-Time', 'Finanças FY24', 'Marketing Digital', 'Controle de Estoque'],
        'Descricao': [
            'Acompanhamento de vendas por região e produto com análise YoY.',
            'Headcount, turnover e métricas de desempenho de colaboradores.',
            'Rastreamento de frota e status de entregas em tempo real.',
            'DRE, Fluxo de Caixa e indicadores de rentabilidade.',
            'Performance de campanhas, ROI e análise de leads.',
            'Giro de estoque, curva ABC e previsão de demanda.'
        ],
        'Link': ['https://google.com'] * 6,
        'Status': ['Ativo', 'Ativo', 'Em Manutenção', 'Ativo', 'Ativo', 'Ativo'],
        'Publico': ['Comercial', 'RH', 'Operações', 'Diretoria', 'Marketing', 'Logística'],
        'Midia': ['PowerBI', 'Tableau', 'PowerBI', 'Excel', 'Google Data Studio', 'Qlik'],
        'Responsavel': ['Ana Silva', 'Carlos Souza', 'Mariana Lima', 'Roberto Alves', 'Julia Costa', 'Pedro Santos'],
        'Periodicidade': ['Diária', 'Mensal', 'Em Tempo Real', 'Mensal', 'Semanal', 'Diária']
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=600)
def load_data():
    """Carrega dados da planilha ou usa mock data."""
    try:
        if "GOOGLE_SHEET_URL" in st.secrets:
            url = st.secrets["GOOGLE_SHEET_URL"]
            # Garante que a URL é de exportação CSV se for Link do Google Sheets
            if "docs.google.com" in url and "/edit" in url:
                url = url.replace("/edit#gid=", "/export?format=csv&gid=")
            
            df = pd.read_csv(url, encoding='utf-8')
        else:
            df = get_mock_data()
        
        # Tratamento de Nulos
        cols_required = ['Nome_Dash', 'Descricao', 'Link', 'Status', 'Publico', 'Midia', 'Responsavel', 'Periodicidade']
        for col in cols_required:
            if col not in df.columns:
                df[col] = "N/A"
        
        df.fillna("N/A", inplace=True)
        return df.astype(str)
        
    except Exception as e:
        st.warning(f"Usando dados de demonstração (Erro na conexão: {str(e)})")
        return get_mock_data().astype(str)

def generate_access_logs():
    """Gera logs simulados."""
    dates = pd.date_range(end=datetime.now(), periods=90).tolist()
    data = []
    
    dashboards = ["Relatório de Vendas", "Análise de RH", "Dashboard Logístico", "Financeiro Consolidado"]
    users = [f"user_{i:03d}@empresa.com" for i in range(1, 20)]
    departments = ["Vendas", "Marketing", "Financeiro", "RH", "TI"]
    
    for date in dates:
        count = random.randint(5, 25)
        for _ in range(count):
            data.append({
                "Data": date,
                "Dashboard": random.choice(dashboards),
                "Usuario": random.choice(users),
                "Departamento": random.choice(departments),
                "Hora": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}"
            })
    
    df_logs = pd.DataFrame(data)
    df_logs['Data'] = pd.to_datetime(df_logs['Data'])
    return df_logs

# Carga Inicial
df_full = load_data()
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else pd.DataFrame()

def get_filter_options(column):
    if df_active.empty: return ["Todos"]
    return ["Todos"] + sorted(df_active[column].unique().tolist())

# ==============================================================================
# COMPONENTES DE UI
# ==============================================================================
def render_kpi_card(label, value, icon, color="#0ea5e9"):
    return f"""
    <div class="kpi-box">
        <i class="fa-solid {icon}" style="font-size: 1.8rem; color: {color}; margin-bottom: 10px;"></i>
        <div class="kpi-val">{value}</div>
        <div class="kpi-lbl">{label}</div>
    </div>
    """

def render_dashboard_card(row):
    """Renderiza HTML do cartão."""
    midia_map = {
        'powerbi': 'fa-chart-bar', 'tableau': 'fa-chart-pie', 
        'excel': 'fa-file-excel', 'google': 'fa-chart-line', 
        'qlik': 'fa-chart-area', 'looker': 'fa-chart-scatter'
    }
    
    midia_clean = row['Midia'].lower()
    icon = next((v for k, v in midia_map.items() if k in midia_clean), 'fa-chart-simple')
    
    link_valid = row['Link'] not in ["N/A", "nan", "", "None"]
    link_html = f'<a href="{row["Link"]}" target="_blank" class="btn-access"><i class="fa-solid fa-external-link-alt"></i> Acessar</a>' if link_valid else \
                '<button class="btn-access btn-disabled" disabled>Indisponível</button>'
    
    freq_class = "badge-success" if "Diária" in row['Periodicidade'] or "Real" in row['Periodicidade'] else "badge-warning"

    html = f"""
    <div class="dashboard-card">
        <div class="card-header">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <h4 style="margin:0; font-size: 1.1rem;">{row['Nome_Dash']}</h4>
                <i class="fa-solid {icon}" style="color: #0ea5e9; font-size: 1.4rem;"></i>
            </div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 5px;">
                <i class="fa-regular fa-user"></i> {row['Responsavel']}
            </div>
        </div>
        <div class="card-body">
            <p style="font-size: 0.9rem; margin: 0; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
                {row['Descricao']}
            </p>
            <div style="margin-top: auto; display: flex; flex-wrap: wrap; gap: 5px;">
                <span class="tech-badge"><i class="fa-solid fa-desktop"></i> {row['Midia']}</span>
                <span class="tech-badge {freq_class}"><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</span>
            </div>
        </div>
        <div class="card-footer">
            {link_html}
        </div>
    </div>
    <div style="margin-bottom: 20px;"></div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# PÁGINAS
# ==============================================================================
def render_sidebar():
    st.sidebar.markdown("### Intelligence Hub")
    st.sidebar.markdown('<div style="text-align: center; margin-bottom: 2rem;"><i class="fa-solid fa-chart-network" style="font-size: 3rem; color: #0ea5e9;"></i></div>', unsafe_allow_html=True)
    
    # Navegação
    options = {"Lobby Principal": "home", "Catálogo": "catalog", "Administração": "admin"}
    
    # Determinar index baseado no estado atual
    current_idx = list(options.values()).index(st.session_state.page) if st.session_state.page in options.values() else 0
    
    selected = st.sidebar.radio("Navegação", list(options.keys()), index=current_idx)
    st.session_state.page = options[selected]
    
    st.sidebar.markdown("---")
    
    filters = ("Todos", "Todos", "Todos", "Todos")
    if st.session_state.page == "catalog":
        st.sidebar.markdown('<div style="color: #0ea5e9; font-weight: 600; margin-bottom: 10px;">FILTROS AVANÇADOS</div>', unsafe_allow_html=True)
        with st.sidebar.container():
            f1 = st.selectbox("Público Alvo", get_filter_options("Publico"))
            f2 = st.selectbox("Plataforma", get_filter_options("Midia"))
            f3 = st.selectbox("Responsável", get_filter_options("Responsavel"))
            f4 = st.selectbox("Periodicidade", get_filter_options("Periodicidade"))
            filters = (f1, f2, f3, f4)
            
            st.sidebar.markdown(f'<div style="text-align:center; font-size:0.8rem; margin-top:20px; color:#64748b">{len(df_active)} Dashboards</div>', unsafe_allow_html=True)
    
    return filters

def page_home():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Hub de Inteligência Corporativa</h1>
        <p style="max-width: 600px; margin: 0 auto; color: #94a3b8;">
            Central de indicadores estratégicos e operacionais para suporte à tomada de decisão.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_active.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(render_kpi_card("Dashboards Ativos", len(df_active), "fa-chart-line"), unsafe_allow_html=True)
        c2.markdown(render_kpi_card("Plataformas", df_active['Midia'].nunique(), "fa-layer-group", "#10b981"), unsafe_allow_html=True)
        c3.markdown(render_kpi_card("Áreas Atendidas", df_active['Publico'].nunique(), "fa-users", "#f59e0b"), unsafe_allow_html=True)
        c4.markdown(render_kpi_card("Atualizações Diárias", len(df_active[df_active['Periodicidade'].str.contains('Diária|Real', case=False)]), "fa-bolt", "#8b5cf6"), unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.write("")
        if st.button("Acessar Catálogo Completo", type="primary", use_container_width=True):
            st.session_state.page = "catalog"
            st.rerun()

def page_catalog(filters):
    pub, mid, resp, perio = filters
    st.title("Catálogo de Soluções")
    
    # Busca e Limpeza
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input("Busca", placeholder="Pesquise por nome, descrição...", label_visibility="collapsed")
    with col2:
        if st.button("Limpar", use_container_width=True):
            st.rerun() # Simplificado para rerun, idealmente resetaria session_state dos filtros

    # Filtragem
    df_view = df_active.copy()
    
    if search:
        term = search.lower()
        df_view = df_view[
            df_view['Nome_Dash'].str.lower().str.contains(term) | 
            df_view['Descricao'].str.lower().str.contains(term)
        ]
    
    if pub != "Todos": df_view = df_view[df_view['Publico'] == pub]
    if mid != "Todos": df_view = df_view[df_view['Midia'] == mid]
    if resp != "Todos": df_view = df_view[df_view['Responsavel'] == resp]
    if perio != "Todos": df_view = df_view[df_view['Periodicidade'] == perio]
    
    if df_view.empty:
        st.info("Nenhum dashboard encontrado com os filtros selecionados.")
        return

    # Renderização em Grid
    cols_per_row = 3
    rows = [df_view.iloc[i:i + cols_per_row] for i in range(0, len(df_view), cols_per_row)]
    
    for row_data in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, dashboard) in enumerate(row_data.iterrows()):
            with cols[idx]:
                render_dashboard_card(dashboard)

def page_admin():
    if not st.session_state.admin_logged:
        st.markdown('<div class="admin-login"><h3 style="text-align:center;">Acesso Restrito</h3>', unsafe_allow_html=True)
        pwd = st.text_input("Senha Administrativa", type="password")
        
        # Tenta pegar senha dos secrets, se falhar usa 'admin' como padrão para evitar travamento
        correct_pass = st.secrets.get("ADMIN_PASSWORD", "admin")
        
        if st.button("Entrar", type="primary", use_container_width=True):
            if pwd == correct_pass:
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Senha incorreta")
        
        if correct_pass == "admin":
            st.caption("⚠️ Modo Demo: A senha é 'admin'")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Dashboard Admin
    c1, c2 = st.columns([5, 1])
    c1.title("Analytics da Plataforma")
    if c2.button("Sair", type="secondary"):
        st.session_state.admin_logged = False
        st.rerun()

    df_logs = generate_access_logs()
    
    # KPI Admin
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Acessos Totais", len(df_logs))
    k2.metric("Usuários Únicos", df_logs['Usuario'].nunique())
    k3.metric("Média Diária", int(len(df_logs)/90))
    k4.metric("Dashboards Monitorados", len(df_active))
    
    st.divider()
    
    t1, t2 = st.tabs(["Tendência de Acesso", "Top Dashboards"])
    
    with t1:
        daily = df_logs.groupby(df_logs['Data'].dt.date).size().reset_index(name='Acessos')
        chart = alt.Chart(daily).mark_line(color='#0ea5e9').encode(
            x='Data:T', y='Acessos:Q', tooltip=['Data', 'Acessos']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)
        
    with t2:
        top = df_logs['Dashboard'].value_counts().reset_index()
        top.columns = ['Dashboard', 'Acessos']
        chart_bar = alt.Chart(top.head(10)).mark_bar().encode(
            x='Acessos:Q', y=alt.Y('Dashboard:N', sort='-x'), color=alt.value('#0ea5e9')
        ).properties(height=300)
        st.altair_chart(chart_bar, use_container_width=True)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    filters = render_sidebar()
    
    if st.session_state.page == "home":
        page_home()
    elif st.session_state.page == "catalog":
        page_catalog(filters)
    elif st.session_state.page == "admin":
        page_admin()

if __name__ == "__main__":
    main()