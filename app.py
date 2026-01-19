import streamlit as st
import pandas as pd
import numpy as np
import os
import csv
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# ==============================================================================
# 1. CONFIGURAÇÃO INICIAL E CONSTANTES
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub | BI Corporativo",
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arquivo onde os cliques reais serão salvos
LOG_FILE = "log_acessos.csv"

# Tema de Cores
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
# 2. FUNÇÕES DE LOG (O CORAÇÃO DO RASTREAMENTO)
# ==============================================================================

def init_log_db():
    """Cria o arquivo CSV de logs se ele não existir."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Data", "Dashboard", "Usuario", "Departamento"])

def registrar_clique(dashboard_name, usuario, departamento):
    """Salva o clique no arquivo CSV."""
    init_log_db()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([agora, dashboard_name, usuario, departamento])

# ==============================================================================
# 3. ESTILIZAÇÃO CSS (Adaptado para Botões Nativos)
# ==============================================================================
def load_custom_css():
    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        .stApp {{ background-color: {THEME['bg_body']}; font-family: 'Inter', sans-serif; }}
        h1, h2, h3 {{ color: {THEME['text_main']} !important; font-weight: 600; }}
        
        /* Cards Visuais */
        .dash-card-top {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            border-bottom: none;
            border-radius: 10px 10px 0 0;
            padding: 20px;
            height: 140px; /* Altura fixa para alinhar */
        }}
        
        .dash-card-bottom {{
            background-color: rgba(0,0,0,0.2);
            border: 1px solid {THEME['border']};
            border-top: none;
            border-radius: 0 0 10px 10px;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        /* Estilizando o Botão Nativo do Streamlit para parecer Customizado */
        div.stButton > button {{
            background-color: {THEME['accent']};
            color: white;
            border: none;
            width: 100%;
            font-weight: 600;
            transition: all 0.3s;
        }}
        div.stButton > button:hover {{
            background-color: #0284c7;
            transform: translateY(-2px);
        }}
        
        /* KPI Cards */
        .kpi-container {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: {THEME['text_main']}; }}
        .kpi-label {{ font-size: 0.8rem; color: {THEME['text_muted']}; text-transform: uppercase; }}

    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ==============================================================================
# 4. CARREGAMENTO DE DADOS
# ==============================================================================
if 'view' not in st.session_state: st.session_state.view = 'landing'
if 'selected_filter' not in st.session_state: st.session_state.selected_filter = "Todos"
if 'admin_logged' not in st.session_state: st.session_state.admin_logged = False

@st.cache_data(ttl=600)
def get_data():
    # Aqui entraria sua conexão real com Google Sheets
    # Para o exemplo funcionar, usamos dados fixos do catálogo
    return pd.DataFrame({
        'Nome_Dash': ['Vendas Gerais', 'Logística SP', 'RH Analytics', 'Financeiro Q1', 'Marketing Performance', 'Estoque CD'],
        'Descricao': ['Análise de sell-out e performance mensal', 'Tracking de entregas e frota', 'Headcount e turnover', 'DRE e fluxo de caixa', 'ROI de campanhas Google/Meta', 'Giro de estoque e ruptura'],
        'Link': ['https://google.com', 'https://google.com', 'https://google.com', 'https://google.com', 'https://google.com', 'https://google.com'],
        'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
        'Responsavel': ['João Silva', 'Maria B.', 'Carlos T.', 'Ana L.', 'Pedro H.', 'Mariana G.'],
        'Publico': ['Comercial', 'Operações', 'RH', 'Financeiro', 'Marketing', 'Logística'],
        'Midia': ['Power BI', 'Excel', 'Looker', 'Power BI', 'Google Ads', 'Power BI'],
        'Periodicidade': ['Diário', 'Tempo Real', 'Mensal', 'Semanal', 'Diário', 'Tempo Real']
    })

df_active = get_data()

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
                <div style="font-size: 1.2rem; color: {THEME['accent']}; margin-bottom: 5px;"><i class="fa-solid {icon}"></i></div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 6. PÁGINAS DO SISTEMA
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
                <p style="color: {THEME['text_muted']}; font-size: 1.2rem;">Portal de BI com rastreamento de uso em tempo real.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid de botões
    publicos = sorted(list(set(df_active['Publico'].unique())))
    cols = st.columns(4)
    for i, setor in enumerate(publicos):
        with cols[i % 4]:
            if st.button(setor, key=f"land_{setor}", use_container_width=True):
                st.session_state.selected_filter = setor
                st.session_state.view = 'gallery'
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns([1,2,1])
    with cb2:
        if st.button("Área Administrativa (Logs Reais)", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()

# --- GALERIA COM RASTREAMENTO REAL ---
def render_gallery():
    # Sidebar e Filtros
    with st.sidebar:
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            st.session_state.view = 'landing'
            st.rerun()
        st.markdown("---")
        
        # Filtro Público
        opts_pub = ["Todos"] + sorted(list(df_active['Publico'].unique()))
        idx = opts_pub.index(st.session_state.selected_filter) if st.session_state.selected_filter in opts_pub else 0
        filtro_pub = st.selectbox("Departamento", opts_pub, index=idx)
        st.session_state.selected_filter = filtro_pub
        
        filtro_tech = st.multiselect("Tecnologia", df_active['Midia'].unique())

    # Conteúdo Principal
    render_header("Catálogo de Dashboards", f"Setor: {st.session_state.selected_filter}")

    # Filtragem
    df_show = df_active.copy()
    if filtro_pub != "Todos": df_show = df_show[df_show['Publico'] == filtro_pub]
    if filtro_tech: df_show = df_show[df_show['Midia'].isin(filtro_tech)]

    if df_show.empty:
        st.warning("Nenhum item encontrado.")
        return

    # Loop de Cards (Grid 3 Colunas)
    cols = st.columns(3)
    for i, row in enumerate(df_show.to_dict('records')):
        with cols[i % 3]:
            # Parte 1: HTML Visual (Título e Descrição)
            icon = "fa-chart-pie"
            if "excel" in row['Midia'].lower(): icon = "fa-file-excel"
            elif "power" in row['Midia'].lower(): icon = "fa-chart-bar"

            st.markdown(f"""
            <div class="dash-card-top">
                <div style="font-weight: 700; font-size: 1.1rem; color: {THEME['text_main']}; margin-bottom: 8px;">
                    <i class="fa-solid {icon}" style="color: {THEME['accent']}"></i> {row['Nome_Dash']}
                </div>
                <div style="font-size: 0.9rem; color: {THEME['text_muted']}; line-height: 1.4;">
                    {row['Descricao']}
                </div>
                <div style="margin-top: 10px;">
                    <span style="font-size: 0.7rem; background: rgba(14,165,233,0.1); color: {THEME['accent']}; padding: 3px 8px; border-radius: 4px;">{row['Midia']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Parte 2: Botão Nativo do Streamlit (Para rastrear o clique)
            # Usamos st.container para colar o botão no HTML de cima
            with st.container():
                # Botão de Ação
                if st.button(f"Acessar 🚀", key=f"btn_{i}", use_container_width=True):
                    # ---------------------------------------------------------
                    # AQUI ACONTECE A MÁGICA DO RASTREAMENTO
                    # ---------------------------------------------------------
                    registrar_clique(row['Nome_Dash'], "Usuario_Anonimo", row['Publico'])
                    
                    # Abre o link em nova aba usando Javascript
                    js = f"window.open('{row['Link']}', '_blank').focus();"
                    components.html(f"<script>{js}</script>", height=0)
                    
                    st.toast(f"Acesso registrado para {row['Nome_Dash']}!", icon="✅")

            # Parte 3: HTML Footer (Detalhes)
            st.markdown(f"""
            <div class="dash-card-bottom">
                <small style="color:{THEME['text_muted']}"><i class="fa-solid fa-user"></i> {row['Responsavel'].split()[0]}</small>
                <small style="color:{THEME['text_muted']}">{row['Periodicidade']}</small>
            </div>
            <div style="margin-bottom: 20px;"></div>
            """, unsafe_allow_html=True)

# --- ADMIN COM DADOS REAIS ---
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

    # Painel Logado
    with st.sidebar:
        if st.button("Sair"):
            st.session_state.admin_logged = False
            st.session_state.view = 'landing'
            st.rerun()

    render_header("Monitoramento Real", "Dados extraídos do arquivo de log local (log_acessos.csv)")

    # Ler dados REAIS do CSV
    if not os.path.exists(LOG_FILE):
        st.info("Nenhum clique registrado ainda. Acesse a galeria e clique em alguns dashboards para gerar dados.")
        return

    try:
        df_logs = pd.read_csv(LOG_FILE)
        if df_logs.empty:
            st.warning("O arquivo de log existe mas está vazio.")
            return
            
        # Converte coluna de data
        df_logs['Data'] = pd.to_datetime(df_logs['Data'])

        # KPIs Reais
        total_clicks = len(df_logs)
        unique_dashs = df_logs['Dashboard'].nunique()
        top_dash = df_logs['Dashboard'].mode()[0] if not df_logs.empty else "N/A"
        
        # Filtrar acessos de hoje
        hoje = pd.Timestamp.now().normalize()
        clicks_hoje = len(df_logs[df_logs['Data'] >= hoje])

        k1, k2, k3, k4 = st.columns(4)
        card_kpi("fa-mouse-pointer", total_clicks, "Cliques Totais", k1)
        card_kpi("fa-calendar-day", clicks_hoje, "Cliques Hoje", k2)
        card_kpi("fa-trophy", unique_dashs, "Dashboards Distintos", k3)
        
        st.markdown(f"""
        <div class="kpi-container" style="border-color: {THEME['success']};">
            <div style="font-size: 0.8rem; color: {THEME['success']};">MAIS ACESSADO</div>
            <div style="font-size: 1.2rem; font-weight:700; color:white;">{top_dash}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráficos
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("### Acessos por Dashboard")
            st.bar_chart(df_logs['Dashboard'].value_counts())
            
        with col_g2:
            st.markdown("### Evolução no Tempo")
            # Agrupar por hora ou dia dependendo do volume
            logs_timeline = df_logs.set_index('Data').resample('H').size() # Agrupado por Hora
            st.line_chart(logs_timeline)

        st.markdown("### Log Bruto (Últimos 100)")
        st.dataframe(df_logs.sort_values(by="Data", ascending=False).head(100), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao ler arquivo de logs: {e}")

# ==============================================================================
# MAIN
# ==============================================================================
if st.session_state.view == 'landing': render_landing()
elif st.session_state.view == 'gallery': render_gallery()
elif st.session_state.view == 'admin': render_admin()

st.markdown("---")
st.markdown("<div style='text-align:center; color:#64748b; font-size:0.8rem'>Intelligence Hub v2.0 • Tracking Ativo</div>", unsafe_allow_html=True)