import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import streamlit.components.v1 as components
import os

# ==============================================================================
# CONFIGURAÇÃO E ESTADO
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de variáveis de sessão
if 'page' not in st.session_state:
    st.session_state.page = "Lobby"
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False
if 'target_filter' not in st.session_state:
    st.session_state.target_filter = "Todos" # Variável para controlar filtro vindo da Home

# ==============================================================================
# SISTEMA DE LOGS (PERSISTENTE)
# ==============================================================================
LOG_FILE = "access_logs.csv"

def log_access(dashboard_name, user="Visitante", area="Geral"):
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
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            df['Data'] = pd.to_datetime(df['Data'])
            return df
        except: pass
    return pd.DataFrame(columns=["Data", "Dashboard", "Usuario", "Departamento", "Hora"])

def open_url_in_new_tab(url):
    js = f"<script>window.open('{url}', '_blank').focus();</script>"
    components.html(js, height=0, width=0)

# ==============================================================================
# CSS REFINADO (CONTRASTE E ÍCONES)
# ==============================================================================
def load_css():
    theme = {
        "bg_main": "#0f172a",
        "bg_card": "#1e293b",
        "border": "#334155",
        "accent": "#0ea5e9",
        "text_white": "#ffffff"
    }

    css = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        .stApp {{ background-color: {theme['bg_main']}; font-family: 'Inter', sans-serif; }}
        h1, h2, h3 {{ color: {theme['text_white']} !important; font-weight: 700; }}
        p, div, span {{ color: #94a3b8; }}
        
        [data-testid="stSidebar"] {{ background-color: {theme['bg_card']}; border-right: 1px solid {theme['border']}; }}
        
        /* BOTÕES - CORREÇÃO DE CONTRASTE */
        div.stButton > button {{
            color: #ffffff !important;
            background-color: {theme['accent']} !important;
            border: none;
            font-weight: 600 !important;
            padding: 0.6rem 1rem;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.2s;
        }}
        div.stButton > button:hover {{
            background-color: #0284c7 !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(14, 165, 233, 0.3);
            color: #ffffff !important;
        }}
        div.stButton > button p {{ color: #ffffff !important; }} /* Garante texto branco */
        
        /* Botão Desabilitado */
        div.stButton > button:disabled {{
            background-color: #334155 !important;
            color: #64748b !important;
            cursor: not-allowed;
            box-shadow: none;
            transform: none;
        }}

        /* Cards */
        .card-container {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            padding: 1.2rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            transition: border-color 0.2s;
        }}
        .card-container:hover {{ border-color: {theme['accent']}; }}
        
        .tech-badge {{
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;
            padding: 2px 8px; border-radius: 4px; border: 1px solid #334155; color: {theme['accent']};
        }}

        /* KPI Box Clean */
        .kpi-box {{
            background: {theme['bg_card']}; border: 1px solid {theme['border']};
            padding: 1.5rem; border-radius: 8px; text-align: center;
        }}
        
        /* Admin Login */
        .admin-box {{
            max-width: 350px; margin: 5rem auto; padding: 2rem;
            background: {theme['bg_card']}; border: 1px solid {theme['border']}; border-radius: 10px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==============================================================================
# DADOS
# ==============================================================================
def get_mock_data():
    return pd.DataFrame({
        'Nome_Dash': ['Gestão de Vendas', 'Headcount & Turnover', 'Logística Outbound', 'DRE Gerencial', 'Performance Ads', 'Giro de Estoque', 'NPS & Churn', 'OEE Fabril'],
        'Descricao': [
            'Monitoramento de KPIs comerciais, funil de vendas e atingimento de metas.',
            'Indicadores de gente e gestão, absenteísmo e retenção de talentos.',
            'Status de entregas, custo de frete e performance de transportadoras.',
            'Visão financeira consolidada, EBITDA e fluxo de caixa operacional.',
            'Retorno sobre investimento (ROAS) e métricas de campanhas digitais.',
            'Análise de cobertura de estoque e ruptura por centro de distribuição.',
            'Satisfação de clientes e monitoramento de cancelamentos.',
            'Eficiência global dos equipamentos e paradas de linha.'
        ],
        'Link': ['https://google.com'] * 8,
        'Status': ['Ativo', 'Ativo', 'Em Manutenção', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
        'Publico': ['Comercial', 'RH', 'Logística', 'Financeiro', 'Marketing', 'Logística', 'CS', 'Industrial'],
        'Midia': ['PowerBI', 'Tableau', 'PowerBI', 'Excel', 'Looker', 'Qlik', 'Salesforce', 'PowerBI'],
        'Responsavel': ['Ana S.', 'Carlos S.', 'Mariana L.', 'Roberto A.', 'Julia C.', 'Pedro S.', 'Amanda L.', 'Ricardo O.'],
        'Periodicidade': ['Diária', 'Mensal', 'Real Time', 'Mensal', 'Semanal', 'Diária', 'Semanal', 'Real Time']
    })

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
        
        cols = ['Nome_Dash', 'Descricao', 'Link', 'Status', 'Publico', 'Midia', 'Responsavel', 'Periodicidade']
        for col in cols:
            if col not in df.columns: df[col] = "N/A"
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except:
        return get_mock_data().astype(str)

df_full = load_data()
df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy() if not df_full.empty else pd.DataFrame()

# ==============================================================================
# RENDERIZAÇÃO DE COMPONENTES
# ==============================================================================
def render_kpi(label, value, icon_class):
    return f"""
    <div class="kpi-box">
        <i class="{icon_class}" style="font-size: 1.5rem; color: #0ea5e9; margin-bottom: 10px;"></i>
        <div style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9;">{value}</div>
        <div style="font-size: 0.8rem; color: #64748b; text-transform: uppercase;">{label}</div>
    </div>
    """

def render_card(row):
    # Ícones baseados na tecnologia
    tech = row['Midia'].lower()
    icon = "fa-chart-simple"
    if 'powerbi' in tech: icon = "fa-chart-bar"
    elif 'tableau' in tech: icon = "fa-chart-pie"
    elif 'excel' in tech: icon = "fa-file-excel"
    
    st.markdown(f"""
    <div class="card-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin:0; font-size: 1rem; color: #fff;">{row['Nome_Dash']}</h4>
            <i class="fa-solid {icon}" style="color: #0ea5e9;"></i>
        </div>
        <p style="font-size: 0.85rem; height: 3.6em; overflow: hidden; margin-bottom: 1rem;">
            {row['Descricao']}
        </p>
        <div style="margin-top: auto; display: flex; gap: 8px; margin-bottom: 15px;">
            <span class="tech-badge">{row['Midia']}</span>
            <span class="tech-badge" style="border-color: #334155; color: #94a3b8;">{row['Publico']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Botão Nativo para ação
    if row['Link'] not in ["N/A", "", "None"]:
        if st.button("Acessar", key=f"btn_{row['Nome_Dash']}", use_container_width=True):
            log_access(row['Nome_Dash'], area=row['Publico'])
            open_url_in_new_tab(row['Link'])
    else:
        st.button("Indisponível", key=f"dis_{row['Nome_Dash']}", disabled=True, use_container_width=True)
        
    st.markdown("</div><div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# ==============================================================================
# PÁGINAS
# ==============================================================================
def render_sidebar():
    st.sidebar.markdown("""
        <div style="text-align:center; padding: 1rem 0 2rem 0;">
            <i class="fa-solid fa-chart-network" style="font-size: 2.5rem; color: #0ea5e9;"></i>
            <h3 style="margin-top: 10px; font-size: 1.1rem;">Intelligence Hub</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu Limpo (Sem emojis)
    pages = ["Lobby", "Catálogo", "Admin"]
    
    # Se a página foi mudada externamente (ex: botão da home), atualiza o índice
    try:
        default_index = pages.index(st.session_state.page)
    except:
        default_index = 0
        
    selected = st.sidebar.radio("Navegação", pages, index=default_index, label_visibility="collapsed")
    
    # Atualiza a sessão apenas se houver mudança manual no radio
    if selected != st.session_state.page:
        st.session_state.page = selected
        # Se usuário clicou manualmente no catálogo, limpa o filtro vindo da home
        if selected == "Catálogo" and "manual_nav" not in st.session_state:
             st.session_state.target_filter = "Todos"
        st.rerun()

    st.sidebar.markdown("---")
    
    # Filtros aparecem apenas no Catálogo
    filters = None
    if st.session_state.page == "Catálogo":
        st.sidebar.markdown('<div style="color:#0ea5e9; font-weight:600; font-size:0.8rem; margin-bottom:10px;">FILTRAR POR</div>', unsafe_allow_html=True)
        
        # Prepara lista de opções e define o index baseado na seleção da Home
        opts_pub = ["Todos"] + sorted(df_active['Publico'].unique().tolist())
        try:
            idx_pub = opts_pub.index(st.session_state.target_filter)
        except:
            idx_pub = 0
            
        with st.sidebar.container():
            f_pub = st.selectbox("Departamento", opts_pub, index=idx_pub)
            f_mid = st.selectbox("Tecnologia", ["Todos"] + sorted(df_active['Midia'].unique().tolist()))
            filters = (f_pub, f_mid)
            
            # Se o usuário mudar o selectbox manualmente, atualiza o state target
            if f_pub != st.session_state.target_filter:
                st.session_state.target_filter = f_pub

    return filters

def page_lobby():
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 3rem 0;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Hub de Inteligência Corporativa</h1>
        <p style="font-size: 1.1rem;">Acesse os indicadores estratégicos da companhia.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. KPIs Gerais
    c1, c2, c3 = st.columns(3)
    c1.markdown(render_kpi("Dashboards Disponíveis", len(df_active), "fa-solid fa-layer-group"), unsafe_allow_html=True)
    c2.markdown(render_kpi("Áreas Atendidas", df_active['Publico'].nunique(), "fa-solid fa-users"), unsafe_allow_html=True)
    c3.markdown(render_kpi("Plataformas Integradas", df_active['Midia'].nunique(), "fa-solid fa-server"), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 2. Navegação por Time (Botões Grandes)
    st.markdown('<h3 style="margin-bottom: 1.5rem; display:flex; align-items:center; gap:10px;"><i class="fa-solid fa-compass" style="color:#0ea5e9;"></i> Navegue por Departamento</h3>', unsafe_allow_html=True)
    
    areas = sorted(df_active['Publico'].unique())
    
    # Grid de botões
    cols = st.columns(4)
    for i, area in enumerate(areas):
        # Usando botão nativo com container_width
        if cols[i % 4].button(f"{area}", use_container_width=True):
            st.session_state.target_filter = area
            st.session_state.page = "Catálogo"
            st.session_state.manual_nav = False # Flag para indicar navegação automática
            st.rerun()

def page_catalog(filters):
    f_pub, f_mid = filters
    
    st.markdown(f"### 📂 Catálogo: {f_pub if f_pub != 'Todos' else 'Geral'}")
    
    # Busca
    c1, c2 = st.columns([4, 1])
    search = c1.text_input("Busca rápida", placeholder="Nome do relatório...", label_visibility="collapsed")
    if c2.button("Limpar", use_container_width=True):
        st.session_state.target_filter = "Todos"
        st.rerun()
    
    # Filtros
    df_view = df_active.copy()
    
    if f_pub != "Todos": df_view = df_view[df_view['Publico'] == f_pub]
    if f_mid != "Todos": df_view = df_view[df_view['Midia'] == f_mid]
    
    if search:
        t = search.lower()
        df_view = df_view[df_view['Nome_Dash'].str.lower().str.contains(t) | df_view['Descricao'].str.lower().str.contains(t)]

    if df_view.empty:
        st.info("Nenhum dashboard encontrado com estes filtros.")
        return

    # Render Grid
    rows = [df_view.iloc[i:i + 3] for i in range(0, len(df_view), 3)]
    for row_data in rows:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(row_data.iterrows()):
            with cols[idx]:
                render_card(row)

def page_admin():
    if not st.session_state.admin_logged:
        st.markdown('<div class="admin-box"><h3 style="text-align:center;">Admin Login</h3>', unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Acessar Painel", use_container_width=True):
            if pwd == st.secrets.get("ADMIN_PASSWORD", "admin"):
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Senha incorreta")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Admin Header
    c1, c2 = st.columns([6, 1])
    c1.title("Painel Administrativo")
    if c2.button("Logout", type="secondary"):
        st.session_state.admin_logged = False
        st.rerun()

    df_logs = load_access_logs()
    
    if df_logs.empty:
        st.warning("Sem dados de log registrados.")
        return

    # Gráficos Temporais
    st.markdown("---")
    t1, t2, t3 = st.tabs(["Diário", "Semanal", "Mensal"])
    
    df_chart = df_logs.set_index('Data')
    
    with t1:
        d_data = df_chart.resample('D').count()['Dashboard'].reset_index(name='Acessos')
        c = alt.Chart(d_data).mark_line(point=True, color='#0ea5e9').encode(x='Data:T', y='Acessos:Q').properties(height=300)
        st.altair_chart(c, use_container_width=True)
    
    with t2:
        w_data = df_chart.resample('W').count()['Dashboard'].reset_index(name='Acessos')
        c = alt.Chart(w_data).mark_bar(color='#10b981').encode(x='Data:T', y='Acessos:Q').properties(height=300)
        st.altair_chart(c, use_container_width=True)
        
    with t3:
        m_data = df_chart.resample('M').count()['Dashboard'].reset_index(name='Acessos')
        c = alt.Chart(m_data).mark_bar(color='#8b5cf6').encode(x='Data:T', y='Acessos:Q').properties(height=300)
        st.altair_chart(c, use_container_width=True)
    
    # Tabela de Dados
    st.markdown("#### Histórico Recente")
    st.dataframe(df_logs.sort_values('Data', ascending=False).head(50), use_container_width=True)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    filters = render_sidebar()
    
    if st.session_state.page == "Lobby":
        page_lobby()
    elif st.session_state.page == "Catálogo":
        page_catalog(filters)
    elif st.session_state.page == "Admin":
        page_admin()

if __name__ == "__main__":
    main()