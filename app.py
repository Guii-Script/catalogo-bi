import streamlit as st
import pandas as pd
import numpy as np
import os
import csv
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# ==============================================================================
# 1. CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub | BI Corporativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arquivo local para salvar os cliques (Bando de dados simples)
LOG_FILE = "log_acessos.csv"

# Seu Tema Original (Mantido)
THEME = {
    "bg_body": "#0f172a",       # Slate 900
    "bg_card": "#1e293b",       # Slate 800
    "border": "#334155",        # Slate 700
    "accent": "#0ea5e9",        # Sky 500
    "text_main": "#f8fafc",     # Slate 50
    "text_muted": "#94a3b8",    # Slate 400
    "success": "#10b981",       # Emerald 500
    "danger": "#ef4444",        # Red 500
}

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASS", "admin123")

# ==============================================================================
# 2. FUNÇÕES DE RASTREAMENTO (LOGS REAIS)
# ==============================================================================
def init_log_db():
    """Cria o arquivo CSV se não existir."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Data", "Dashboard", "Usuario", "Departamento"])

def registrar_clique(dashboard, usuario, departamento):
    """Salva o clique no arquivo local."""
    init_log_db()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([agora, dashboard, usuario, departamento])

# ==============================================================================
# 3. CSS (DESIGN ORIGINAL + AJUSTE DO BOTÃO)
# ==============================================================================
def load_custom_css():
    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        .stApp {{ background-color: {THEME['bg_body']}; font-family: 'Inter', sans-serif; }}
        h1, h2, h3 {{ color: {THEME['text_main']} !important; font-weight: 600; }}
        
        /* Card Container */
        .dash-card-container {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            border-radius: 10px;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            transition: border 0.3s ease;
        }}
        .dash-card-container:hover {{ border-color: {THEME['accent']}; }}

        /* Topo do Card (HTML) */
        .card-top {{
            padding: 20px;
            background: linear-gradient(to right, rgba(15, 23, 42, 0.5), transparent);
            flex-grow: 1;
        }}
        
        /* Rodapé do Card (HTML) */
        .card-bottom {{
            padding: 15px 20px;
            background-color: rgba(0,0,0,0.2);
            border-top: 1px solid {THEME['border']};
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        /* HACK: Estilizando o botão nativo do Streamlit para parecer seu botão customizado */
        div.stButton > button {{
            width: 100%;
            background-color: {THEME['accent']};
            color: white;
            border: none;
            padding: 8px 16px;
            font-weight: 500;
            border-radius: 6px;
            transition: all 0.2s;
        }}
        div.stButton > button:hover {{
            background-color: #0284c7;
            transform: translateY(-2px);
            color: white;
        }}
        div.stButton > button:active {{
            background-color: {THEME['success']};
        }}

        /* KPI Cards */
        .kpi-container {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .kpi-value {{ font-size: 2rem; font-weight: 700; color: {THEME['text_main']}; }}
        .kpi-label {{ font-size: 0.85rem; color: {THEME['text_muted']}; text-transform: uppercase; margin-top: 5px; }}
        
        /* Landing Grid */
        .landing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: 40px; }}
        
        /* Badges */
        .tech-badge {{
            background-color: rgba(14, 165, 233, 0.1);
            color: {THEME['accent']};
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(14, 165, 233, 0.2);
        }}
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ==============================================================================
# 4. DADOS
# ==============================================================================
if 'view' not in st.session_state: st.session_state.view = 'landing'
if 'selected_filter' not in st.session_state: st.session_state.selected_filter = "Todos"
if 'admin_logged' not in st.session_state: st.session_state.admin_logged = False

@st.cache_data(ttl=600)
def get_data():
    try:
        url = st.secrets.get("GOOGLE_SHEET_URL")
        if url:
            df = pd.read_csv(url)
            df.fillna("N/A", inplace=True)
            return df
        else:
            # Fallback para caso não tenha secrets configurado
            # (Adicionei mais exemplos para não parecer vazio)
            return pd.DataFrame({
                'Nome_Dash': ['Vendas Gerais', 'Logística SP', 'RH Analytics', 'Financeiro Q1', 'Marketing Performance', 'Estoque CD', 'CRM Clientes', 'Produção Fabril'],
                'Descricao': ['Análise de sell-out e performance', 'Tracking de entregas e frota', 'Headcount e turnover', 'DRE e fluxo de caixa', 'ROI Google/Meta', 'Giro de estoque e ruptura', 'Funil de vendas e leads', 'OEE e paradas de máquina'],
                'Link': ['https://google.com'] * 8,
                'Status': ['Ativo', 'Ativo', 'Manutenção', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
                'Responsavel': ['João S.', 'Maria B.', 'Carlos T.', 'Ana L.', 'Pedro H.', 'Mariana G.', 'Lucas F.', 'Julia R.'],
                'Publico': ['Comercial', 'Operações', 'RH', 'Financeiro', 'Marketing', 'Logística', 'Comercial', 'Industrial'],
                'Midia': ['Power BI', 'Excel', 'Looker', 'Power BI', 'Google Ads', 'Power BI', 'Salesforce', 'Excel'],
                'Periodicidade': ['Diário', 'Real Time', 'Mensal', 'Semanal', 'Diário', 'Real Time', 'Diário', 'Turno']
            })
    except Exception as e:
        st.error(f"Erro de dados: {e}")
        return pd.DataFrame()

df_full = get_data()
# Garante que as colunas existam mesmo se o CSV vier vazio
cols_needed = ['Nome_Dash', 'Descricao', 'Link', 'Status', 'Responsavel', 'Publico', 'Midia', 'Periodicidade']
for col in cols_needed:
    if col not in df_full.columns: df_full[col] = "N/A"

df_active = df_full[df_full['Status'].str.lower() != 'inativo'].copy()

# ==============================================================================
# 5. COMPONENTES VISUAIS
# ==============================================================================
def render_header(title, subtitle):
    st.markdown(f"""
        <div style="margin-bottom: 2rem; border-bottom: 1px solid {THEME['border']}; padding-bottom: 1rem;">
            <h1 style="margin-bottom: 0.5rem;">{title}</h1>
            <p style="color: {THEME['text_muted']};">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def card_kpi(icon, value, label, col):
    with col:
        st.markdown(f"""
            <div class="kpi-container">
                <div style="font-size: 1.5rem; color: {THEME['accent']}; margin-bottom: 10px;"><i class="fa-solid {icon}"></i></div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 6. PÁGINAS
# ==============================================================================

# --- LANDING PAGE ---
def render_landing():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 4rem; color: {THEME['accent']}; margin-bottom: 1rem;"><i class="fa-solid fa-network-wired"></i></div>
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">Intelligence Hub</h1>
                <p style="color: {THEME['text_muted']}; font-size: 1.2rem;">Portal de BI Corporativo.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid de Setores
    if not df_active.empty:
        raw_publicos = df_active['Publico'].unique()
        setores = sorted(list(set([x.strip() for p in raw_publicos for x in str(p).split('/') if x != "N/A"])))
        
        st.markdown('<div class="landing-grid">', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, setor in enumerate(setores):
            with cols[i % 4]:
                if st.button(setor, key=f"land_{setor}", use_container_width=True):
                    st.session_state.selected_filter = setor
                    st.session_state.view = 'gallery'
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns([1,2,1])
    with cb1:
        if st.button("Ver Catálogo Completo", use_container_width=True):
            st.session_state.selected_filter = "Todos"
            st.session_state.view = 'gallery'
            st.rerun()
    with cb3:
        if st.button("Área Admin (Logs Reais)", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()

# --- GALERIA (COM RASTREAMENTO REAL) ---
def render_gallery():
    # Sidebar
    with st.sidebar:
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            st.session_state.view = 'landing'
            st.rerun()
        st.markdown("---")
        opts_pub = ["Todos"] + sorted(list(set([x.strip() for p in df_active['Publico'].unique() for x in str(p).split('/')])))
        idx = opts_pub.index(st.session_state.selected_filter) if st.session_state.selected_filter in opts_pub else 0
        filtro_pub = st.selectbox("Departamento", opts_pub, index=idx)
        st.session_state.selected_filter = filtro_pub
        
        filtro_tech = st.multiselect("Tecnologia", df_active['Midia'].unique())

    # Header
    render_header("Catálogo", f"Filtro: <span style='color:{THEME['accent']}'>{st.session_state.selected_filter}</span>")

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    card_kpi("fa-database", len(df_full), "Total", k1)
    card_kpi("fa-check", len(df_active), "Ativos", k2)
    card_kpi("fa-users", df_active['Responsavel'].nunique(), "Analistas", k3)
    card_kpi("fa-server", df_active['Midia'].nunique(), "Plataformas", k4)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtragem
    df_show = df_active.copy()
    if filtro_pub != "Todos":
        df_show = df_show[df_show['Publico'].str.contains(filtro_pub, na=False)]
    if filtro_tech:
        df_show = df_show[df_show['Midia'].isin(filtro_tech)]

    if df_show.empty:
        st.warning("Nenhum dashboard encontrado.")
        return

    # Renderização (Card Híbrido: HTML + st.button)
    cols = st.columns(3)
    for i, row in enumerate(df_show.to_dict('records')):
        with cols[i % 3]:
            # Ícone
            midia = str(row['Midia']).lower()
            icon = "fa-chart-pie"
            if "excel" in midia: icon = "fa-file-excel"
            elif "power" in midia: icon = "fa-chart-bar"

            # 1. Topo do Card (HTML)
            st.markdown(f"""
            <div class="dash-card-container">
                <div class="card-top">
                    <div style="font-weight: 600; font-size: 1.1rem; color: {THEME['text_main']}; margin-bottom: 8px;">
                        <i class="fa-solid {icon}" style="color: {THEME['accent']}"></i> {row['Nome_Dash']}
                    </div>
                    <div style="font-size: 0.9rem; color: {THEME['text_muted']}; min-height: 40px;">
                        {row['Descricao']}
                    </div>
                    <div style="margin-top: 10px;">
                        <span class="tech-badge">{row['Midia']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 2. Botão Funcional (Python) - Inserido no meio do fluxo visual
            # O st.container() ajuda a agrupar, mas o CSS 'div.stButton' faz a mágica visual
            link_valido = row['Link'] and str(row['Link']).lower() not in ['nan', 'n/a', '']
            
            with st.container():
                if link_valido:
                    if st.button(f"Acessar 🚀", key=f"btn_{i}", use_container_width=True):
                        # --- LÓGICA DE RASTREAMENTO ---
                        registrar_clique(row['Nome_Dash'], "Usuario_Anonimo", row['Publico'])
                        # Redirecionamento JS
                        js = f"window.open('{row['Link']}', '_blank').focus();"
                        components.html(f"<script>{js}</script>", height=0)
                        st.toast(f"Redirecionando para {row['Nome_Dash']}...", icon="⏳")
                else:
                    st.button("Indisponível", key=f"btn_{i}", disabled=True, use_container_width=True)

            # 3. Rodapé do Card (HTML) - Fecha a div .dash-card-container
            st.markdown(f"""
                <div class="card-bottom">
                    <small style="color:{THEME['text_muted']}"><i class="fa-solid fa-user"></i> {row['Responsavel'].split()[0]}</small>
                    <small style="color:{THEME['text_muted']}"><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</small>
                </div>
            </div>
            <div style="margin-bottom: 20px;"></div>
            """, unsafe_allow_html=True)

# --- ADMIN COM LOGS REAIS ---
def render_admin():
    if not st.session_state.admin_logged:
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            st.markdown("### Login Admin")
            pwd = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged = True
                    st.rerun()
                else: st.error("Senha incorreta")
            if st.button("Voltar"):
                st.session_state.view = 'landing'
                st.rerun()
        return

    with st.sidebar:
        if st.button("Sair"):
            st.session_state.admin_logged = False
            st.session_state.view = 'landing'
            st.rerun()

    render_header("Admin - Logs Reais", "Monitoramento baseado em cliques no botão 'Acessar'")

    if not os.path.exists(LOG_FILE):
        st.info("O arquivo de logs ainda não foi criado. Acesse a galeria e clique em alguns dashboards.")
        return

    try:
        df_logs = pd.read_csv(LOG_FILE)
        if df_logs.empty:
            st.warning("Nenhum acesso registrado ainda.")
            return

        df_logs['Data'] = pd.to_datetime(df_logs['Data'])
        
        # KPIs
        k1, k2, k3 = st.columns(3)
        card_kpi("fa-mouse-pointer", len(df_logs), "Total Cliques", k1)
        card_kpi("fa-trophy", df_logs['Dashboard'].nunique(), "Dashboards Acessados", k2)
        
        hoje = pd.Timestamp.now().normalize()
        cliques_hoje = len(df_logs[df_logs['Data'] >= hoje])
        card_kpi("fa-calendar-day", cliques_hoje, "Acessos Hoje", k3)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Top Dashboards")
            st.bar_chart(df_logs['Dashboard'].value_counts())
        with c2:
            st.markdown("##### Por Departamento")
            st.bar_chart(df_logs['Departamento'].value_counts())
            
        st.markdown("##### Histórico Completo")
        st.dataframe(df_logs.sort_values(by='Data', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao ler logs: {e}")

# ==============================================================================
# MAIN
# ==============================================================================
if st.session_state.view == 'landing': render_landing()
elif st.session_state.view == 'gallery': render_gallery()
elif st.session_state.view == 'admin': render_admin()

st.markdown("---")
st.markdown("<div style='text-align:center; color:#64748b; font-size:0.8rem'>Intelligence Hub • Tracking Ativo</div>", unsafe_allow_html=True)