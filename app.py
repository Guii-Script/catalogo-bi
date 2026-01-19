import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import streamlit.components.v1 as components
import os

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
# SISTEMA DE LOGS (REAL)
# ==============================================================================
LOG_FILE = "access_logs.csv"

def log_access(dashboard_name, user="Visitante", area="Geral"):
    """Registra o acesso no arquivo CSV."""
    new_entry = {
        "Data": datetime.now(),
        "Dashboard": dashboard_name,
        "Usuario": user,
        "Departamento": area,
        "Hora": datetime.now().strftime("%H:%M")
    }
    
    df_new = pd.DataFrame([new_entry])
    
    if not os.path.exists(LOG_FILE):
        df_new.to_csv(LOG_FILE, index=False)
    else:
        df_new.to_csv(LOG_FILE, mode='a', header=False, index=False)

def load_access_logs():
    """Lê os logs reais do CSV."""
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            df['Data'] = pd.to_datetime(df['Data'])
            return df
        except Exception:
            return pd.DataFrame(columns=["Data", "Dashboard", "Usuario", "Departamento", "Hora"])
    return pd.DataFrame(columns=["Data", "Dashboard", "Usuario", "Departamento", "Hora"])

def open_url_in_new_tab(url):
    """Abre URL em nova aba usando JavaScript."""
    js = f"""
    <script>
        window.open('{url}', '_blank').focus();
    </script>
    """
    components.html(js, height=0, width=0)

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
        
        .stApp {{ background-color: {theme['bg_main']}; font-family: 'Inter', sans-serif; }}
        h1, h2, h3, h4 {{ color: {theme['text_head']} !important; font-weight: 600; }}
        p, label, span, div {{ color: {theme['text_body']}; }}
        
        [data-testid="stSidebar"] {{ background-color: {theme['bg_card']}; border-right: 1px solid {theme['border']}; }}
        
        .hero-container {{
            text-align: center; padding: 4rem 1rem;
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
        
        /* Estrutura do Card Híbrido */
        .card-container {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 12px;
            padding: 0;
            overflow: hidden;
            transition: transform 0.2s;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        .card-container:hover {{ border-color: {theme['accent']}; transform: translateY(-3px); }}
        
        .card-header {{ padding: 1.25rem; border-bottom: 1px solid {theme['border']}; background-color: rgba(30, 41, 59, 0.5); }}
        .card-body {{ padding: 1.25rem; flex-grow: 1; }}
        .card-footer {{ padding: 1rem 1.25rem; background-color: rgba(15, 23, 42, 0.3); border-top: 1px solid {theme['border']}; }}
        
        .tech-badge {{
            display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.25rem 0.75rem;
            border-radius: 9999px; font-size: 0.7rem; font-weight: 600;
            background: {theme['accent_glow']}; color: {theme['accent']}; border: 1px solid rgba(14, 165, 233, 0.3);
        }}
        .badge-success {{ background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.3); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.1); color: #f59e0b; border-color: rgba(245, 158, 11, 0.3); }}

        /* KPI Box */
        .kpi-box {{ background: {theme['bg_card']}; border: 1px solid {theme['border']}; padding: 1.5rem; border-radius: 8px; text-align: center; }}
        .kpi-val {{ font-size: 2rem; font-weight: 700; color: {theme['text_head']}; }}
        .kpi-lbl {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.5rem; }}
        
        /* Ajuste do botão nativo do Streamlit dentro do card */
        div.stButton > button {{
            width: 100%;
            background-color: {theme['accent']};
            color: white;
            border: none;
            padding: 0.6rem;
            font-weight: 500;
        }}
        div.stButton > button:hover {{ background-color: #0284c7; color: white; border-color: #0284c7; }}
        div.stButton > button:focus {{ color: white; }}
        
        .admin-login {{ max-width: 400px; margin: 4rem auto; padding: 2rem; background-color: {theme['bg_card']}; border: 1px solid {theme['border']}; border-radius: 12px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==============================================================================
# DADOS
# ==============================================================================
def get_mock_data():
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
    try:
        if "GOOGLE_SHEET_URL" in st.secrets:
            url = st.secrets["GOOGLE_SHEET_URL"]
            if "docs.google.com" in url and "/edit" in url:
                url = url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(url, encoding='utf-8')
        else:
            df = get_mock_data()
        
        cols_required = ['Nome_Dash', 'Descricao', 'Link', 'Status', 'Publico', 'Midia', 'Responsavel', 'Periodicidade']
        for col in cols_required:
            if col not in df.columns: df[col] = "N/A"
        
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception:
        return get_mock_data().astype(str)

df_full = load_data()
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else pd.DataFrame()

def get_filter_options(column):
    if df_active.empty: return ["Todos"]
    return ["Todos"] + sorted(df_active[column].unique().tolist())

# ==============================================================================
# RENDERIZAÇÃO DE COMPONENTES
# ==============================================================================
def render_kpi_card(label, value, icon, color="#0ea5e9"):
    return f"""
    <div class="kpi-box">
        <i class="fa-solid {icon}" style="font-size: 1.8rem; color: {color}; margin-bottom: 10px;"></i>
        <div class="kpi-val">{value}</div>
        <div class="kpi-lbl">{label}</div>
    </div>
    """

def render_dashboard_card_interactive(row):
    """
    Renderiza o card dividindo o HTML em duas partes para inserir 
    o botão nativo do Streamlit no meio, permitindo o registro do log.
    """
    midia_map = {
        'powerbi': 'fa-chart-bar', 'tableau': 'fa-chart-pie', 
        'excel': 'fa-file-excel', 'google': 'fa-chart-line', 
        'qlik': 'fa-chart-area', 'looker': 'fa-chart-scatter'
    }
    midia_clean = row['Midia'].lower()
    icon = next((v for k, v in midia_map.items() if k in midia_clean), 'fa-chart-simple')
    freq_class = "badge-success" if "Diária" in row['Periodicidade'] or "Real" in row['Periodicidade'] else "badge-warning"
    
    # Parte Superior do HTML
    html_top = f"""
    <div class="card-container">
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
            <p style="font-size: 0.9rem; margin: 0; min-height: 4.5em; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
                {row['Descricao']}
            </p>
            <div style="margin-top: 15px; display: flex; flex-wrap: wrap; gap: 5px;">
                <span class="tech-badge"><i class="fa-solid fa-desktop"></i> {row['Midia']}</span>
                <span class="tech-badge {freq_class}"><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</span>
            </div>
        </div>
        <div class="card-footer">
    """
    
    # Renderizar
    st.markdown(html_top, unsafe_allow_html=True)
    
    # Botão Nativo para registrar Log
    link_valid = row['Link'] not in ["N/A", "nan", "", "None"]
    
    if link_valid:
        # A chave DEVE ser única para cada botão
        if st.button(f"Acessar Dashboard", key=f"btn_{row['Nome_Dash']}", use_container_width=True):
            log_access(row['Nome_Dash'], area=row['Publico'])
            open_url_in_new_tab(row['Link'])
    else:
        st.button("Indisponível", disabled=True, key=f"btn_dis_{row['Nome_Dash']}", use_container_width=True)
        
    # Parte Inferior do HTML (Fechar divs)
    st.markdown("</div></div><div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# PÁGINAS
# ==============================================================================
def render_sidebar():
    st.sidebar.markdown("### Intelligence Hub")
    st.sidebar.markdown('<div style="text-align: center; margin-bottom: 2rem;"><i class="fa-solid fa-chart-network" style="font-size: 3rem; color: #0ea5e9;"></i></div>', unsafe_allow_html=True)
    
    options = {"Lobby Principal": "home", "Catálogo": "catalog", "Administração": "admin"}
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
    
    # Tentar carregar logs reais para estatísticas
    df_logs = load_access_logs()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(render_kpi_card("Dashboards Ativos", len(df_active), "fa-chart-line"), unsafe_allow_html=True)
    c2.markdown(render_kpi_card("Plataformas", df_active['Midia'].nunique(), "fa-layer-group", "#10b981"), unsafe_allow_html=True)
    
    # KPI Dinâmico: Acessos Hoje
    if not df_logs.empty:
        acessos_hoje = len(df_logs[df_logs['Data'].dt.date == datetime.now().date()])
    else:
        acessos_hoje = 0
        
    c3.markdown(render_kpi_card("Acessos Hoje", acessos_hoje, "fa-users", "#f59e0b"), unsafe_allow_html=True)
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
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search = st.text_input("Busca", placeholder="Pesquise por nome, descrição...", label_visibility="collapsed")
    with col2:
        if st.button("Limpar", use_container_width=True): st.rerun()

    df_view = df_active.copy()
    if search:
        term = search.lower()
        df_view = df_view[df_view['Nome_Dash'].str.lower().str.contains(term) | df_view['Descricao'].str.lower().str.contains(term)]
    
    if pub != "Todos": df_view = df_view[df_view['Publico'] == pub]
    if mid != "Todos": df_view = df_view[df_view['Midia'] == mid]
    if resp != "Todos": df_view = df_view[df_view['Responsavel'] == resp]
    if perio != "Todos": df_view = df_view[df_view['Periodicidade'] == perio]
    
    if df_view.empty:
        st.info("Nenhum dashboard encontrado.")
        return

    cols_per_row = 3
    rows = [df_view.iloc[i:i + cols_per_row] for i in range(0, len(df_view), cols_per_row)]
    
    for row_data in rows:
        cols = st.columns(cols_per_row)
        for idx, (_, dashboard) in enumerate(row_data.iterrows()):
            with cols[idx]:
                render_dashboard_card_interactive(dashboard)

def page_admin():
    if not st.session_state.admin_logged:
        st.markdown('<div class="admin-login"><h3 style="text-align:center;">Acesso Restrito</h3>', unsafe_allow_html=True)
        pwd = st.text_input("Senha Administrativa", type="password")
        correct_pass = st.secrets.get("ADMIN_PASSWORD", "admin")
        if st.button("Entrar", type="primary", use_container_width=True):
            if pwd == correct_pass:
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Senha incorreta")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Dashboard Admin - AGORA COM DADOS REAIS
    c1, c2 = st.columns([5, 1])
    c1.title("Analytics da Plataforma")
    if c2.button("Sair", type="secondary"):
        st.session_state.admin_logged = False
        st.rerun()

    df_logs = load_access_logs()
    
    if df_logs.empty:
        st.warning("Nenhum acesso registrado até o momento.")
        return
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Acessos Totais", len(df_logs))
    k2.metric("Top Dashboard", df_logs['Dashboard'].mode()[0] if not df_logs.empty else "N/A")
    
    df_hoje = df_logs[df_logs['Data'].dt.date == datetime.now().date()]
    k3.metric("Acessos Hoje", len(df_hoje))
    
    k4.metric("Dashboards Monitorados", len(df_active))
    
    st.divider()
    
    t1, t2, t3 = st.tabs(["Histórico", "Top Dashboards", "Log Bruto"])
    
    with t1:
        daily = df_logs.groupby(df_logs['Data'].dt.date).size().reset_index(name='Acessos')
        chart = alt.Chart(daily).mark_line(color='#0ea5e9', point=True).encode(
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
        
    with t3:
        st.dataframe(df_logs.sort_values('Data', ascending=False), use_container_width=True)
        
        # Botão para baixar CSV
        csv = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Baixar Logs em CSV",
            csv,
            "access_logs.csv",
            "text/csv",
            key='download-csv'
        )

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    filters = render_sidebar()
    if st.session_state.page == "home": page_home()
    elif st.session_state.page == "catalog": page_catalog(filters)
    elif st.session_state.page == "admin": page_admin()

if __name__ == "__main__":
    main()