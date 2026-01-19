import streamlit as st
import pandas as pd
import numpy as np
import os
import csv
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# ==============================================================================
# 1. CONFIGURAÇÃO (SETUP)
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub",
    page_icon="chart_with_upwards_trend",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LOG_FILE = "log_acessos.csv"

# Paleta de Cores Corporativa (Dark Slate)
THEME = {
    "bg_body": "#0f172a",       # Slate 900
    "bg_card": "#1e293b",       # Slate 800
    "border": "#334155",        # Slate 700
    "accent": "#0ea5e9",        # Sky 500
    "text_main": "#f8fafc",     # Slate 50
    "text_muted": "#94a3b8",    # Slate 400
    "success": "#10b981",       # Emerald
    "warning": "#f59e0b",       # Amber
    "danger": "#ef4444",        # Red
}

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASS", "admin123")

# ==============================================================================
# 2. FUNÇÕES DE BACKEND (LOGS)
# ==============================================================================
def init_log_db():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Data", "Dashboard", "Usuario", "Departamento", "Hora"])

def registrar_clique(dashboard, usuario, departamento):
    init_log_db()
    agora = datetime.now()
    str_data = agora.strftime("%Y-%m-%d %H:%M:%S")
    hora = agora.hour
    
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([str_data, dashboard, usuario, departamento, hora])

# ==============================================================================
# 3. CSS (DESIGN PROFISSIONAL SEM EMOJIS)
# ==============================================================================
def load_css():
    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {{ background-color: {THEME['bg_body']}; font-family: 'Inter', sans-serif; }}
        
        /* Tipografia */
        h1, h2, h3 {{ color: {THEME['text_main']} !important; font-weight: 700; letter-spacing: -0.5px; }}
        p, label, li {{ color: {THEME['text_muted']}; }}
        
        /* Card Principal */
        .dash-card {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            border-radius: 8px;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100%;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .dash-card:hover {{
            border-color: {THEME['accent']};
            transform: translateY(-2px);
        }}
        
        .card-header {{ padding: 1.5rem; flex-grow: 1; }}
        .card-meta {{ 
            padding: 1rem 1.5rem; 
            border-top: 1px solid {THEME['border']}; 
            background: rgba(0,0,0,0.2);
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }}

        /* Badge Tecnológica */
        .tech-tag {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 4px 8px;
            border-radius: 4px;
            background: rgba(14, 165, 233, 0.15);
            color: {THEME['accent']};
            border: 1px solid rgba(14, 165, 233, 0.3);
            font-weight: 600;
        }}

        /* Botão Estilizado (Override do Streamlit) */
        div.stButton > button {{
            width: 100%;
            background-color: {THEME['accent']};
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border-radius: 6px;
            transition: all 0.2s;
        }}
        div.stButton > button:hover {{
            background-color: #0284c7;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        }}
        
        /* KPIs Admin */
        .kpi-box {{
            background: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }}
        .kpi-num {{ font-size: 2rem; font-weight: 700; color: {THEME['text_main']}; }}
        .kpi-txt {{ font-size: 0.85rem; text-transform: uppercase; color: {THEME['text_muted']}; margin-top: 5px; }}

        /* Link de Backup (Fallback) */
        .backup-link {{
            font-size: 0.75rem;
            color: {THEME['text_muted']};
            text-decoration: none;
            margin-top: 5px;
            display: block;
            text-align: center;
        }}
        .backup-link:hover {{ text-decoration: underline; color: {THEME['accent']}; }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==============================================================================
# 4. CARREGAMENTO DE DADOS
# ==============================================================================
if 'view' not in st.session_state: st.session_state.view = 'landing'
if 'selected_filter' not in st.session_state: st.session_state.selected_filter = "Todos"
if 'admin_logged' not in st.session_state: st.session_state.admin_logged = False

@st.cache_data(ttl=600)
def get_data():
    # Simulando base de dados vinda do Google Sheets
    data = {
        'Nome_Dash': ['Vendas Performance', 'Logística Frota', 'Headcount RH', 'DRE Financeiro', 'Campanhas MKT', 'Estoque CD'],
        'Descricao': [
            'Monitoramento de sell-out, metas e performance de vendedores.', 
            'Rastreamento em tempo real de entregas e manutenção de frota.', 
            'Análise de turnover, admissões e custo de folha.', 
            'Fluxo de caixa, DRE gerencial e indicadores de liquidez.', 
            'ROI de campanhas Google Ads e Meta Ads.', 
            'Giro de estoque, ruptura e curva ABC de produtos.'
        ],
        'Link': ['https://google.com'] * 6, # Substituir pelos links reais
        'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
        'Responsavel': ['João S.', 'Maria B.', 'Carlos T.', 'Ana L.', 'Pedro H.', 'Mariana G.'],
        'Publico': ['Comercial', 'Operações', 'RH', 'Financeiro', 'Marketing', 'Logística'],
        'Midia': ['Power BI', 'Excel', 'Looker', 'Power BI', 'Google Ads', 'Power BI'],
        'Periodicidade': ['Diário', 'Real Time', 'Mensal', 'Semanal', 'Diário', 'Real Time']
    }
    return pd.DataFrame(data)

df_active = get_data()

# ==============================================================================
# 5. UI COMPONENTS
# ==============================================================================
def render_header(title, subtitle):
    st.markdown(f"""
        <div style="margin-bottom: 2rem; border-left: 4px solid {THEME['accent']}; padding-left: 1rem;">
            <h1 style="margin:0; font-size: 2.2rem;">{title}</h1>
            <p style="margin:0; font-size: 1rem; margin-top: 0.5rem;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def kpi_card(label, value, icon, trend=None, col=None):
    if col:
        with col:
            color = THEME['text_main']
            if trend:
                color = THEME['success'] if trend > 0 else THEME['danger']
            
            st.markdown(f"""
            <div class="kpi-box">
                <i class="fa-solid {icon}" style="font-size: 1.5rem; color: {THEME['accent']}; margin-bottom: 10px;"></i>
                <div class="kpi-num" style="color:{color}">{value}</div>
                <div class="kpi-txt">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 6. PÁGINAS
# ==============================================================================

# --- LANDING PAGE ---
def render_landing():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
            <div style="text-align: center;">
                <i class="fa-solid fa-layer-group" style="font-size: 4rem; color: {THEME['accent']}; margin-bottom: 1.5rem;"></i>
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">Intelligence Hub</h1>
                <p style="font-size: 1.2rem; line-height: 1.6;">
                    Portal Corporativo de Inteligência de Dados.<br>
                    Selecione sua área para acessar os relatórios.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid de botões
    cols = st.columns(4)
    areas = sorted(df_active['Publico'].unique())
    
    for i, area in enumerate(areas):
        with cols[i % 4]:
            if st.button(area, key=f"btn_land_{area}", use_container_width=True):
                st.session_state.selected_filter = area
                st.session_state.view = 'gallery'
                st.rerun()
                
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_adm_1, col_adm_2, col_adm_3 = st.columns([1,2,1])
    with col_adm_2:
        if st.button("Acesso Administrativo (BI Team)", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()

# --- GALERIA DE DASHBOARDS (COM REDIRECIONAMENTO CORRIGIDO) ---
def render_gallery():
    # Sidebar
    with st.sidebar:
        if st.button("Voltar ao Início", use_container_width=True):
            st.session_state.view = 'landing'
            st.rerun()
        st.markdown("---")
        
        # Filtros
        options_pub = ["Todos"] + sorted(df_active['Publico'].unique().tolist())
        idx = options_pub.index(st.session_state.selected_filter) if st.session_state.selected_filter in options_pub else 0
        sel_pub = st.selectbox("Departamento", options_pub, index=idx)
        st.session_state.selected_filter = sel_pub
        
        sel_tech = st.multiselect("Plataforma", df_active['Midia'].unique())

    # Header
    render_header("Catálogo de Dashboards", f"Filtrando por: {st.session_state.selected_filter}")

    # Filtragem
    df_show = df_active.copy()
    if sel_pub != "Todos": df_show = df_show[df_show['Publico'] == sel_pub]
    if sel_tech: df_show = df_show[df_show['Midia'].isin(sel_tech)]

    if df_show.empty:
        st.warning("Nenhum dashboard encontrado.")
        return

    # Grid Display
    cols = st.columns(3)
    for i, row in enumerate(df_show.to_dict('records')):
        with cols[i % 3]:
            # Ícone baseado na midia
            midia = row['Midia'].lower()
            icon = "fa-chart-pie"
            if "excel" in midia: icon = "fa-file-excel"
            elif "power" in midia: icon = "fa-chart-bar"
            elif "google" in midia: icon = "fa-google"

            # 1. Card Container (HTML Top)
            st.markdown(f"""
            <div class="dash-card">
                <div class="card-header">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
                        <span class="tech-tag">{row['Midia']}</span>
                        <i class="fa-solid {icon}" style="color:{THEME['accent']}; font-size:1.2rem;"></i>
                    </div>
                    <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{row['Nome_Dash']}</h3>
                    <p style="font-size:0.9rem; line-height:1.4;">{row['Descricao']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. Área do Botão (Python + JS Redirect)
            # Usamos st.container para injetar o botão dentro do fluxo visual do card
            with st.container():
                # Botão Principal
                if st.button("ACESSAR SISTEMA", key=f"btn_access_{i}", use_container_width=True):
                    # Passo A: Logar no CSV
                    registrar_clique(row['Nome_Dash'], "Usuario_Anonimo", row['Publico'])
                    
                    # Passo B: Redirecionar via JS
                    # Height=0 esconde o componente iframe
                    js = f"""
                    <script>
                        window.open('{row['Link']}', '_blank');
                    </script>
                    """
                    components.html(js, height=0)
                    st.toast(f"Redirecionando para {row['Nome_Dash']}...", icon=None)

                # Link de Backup caso o popup blocker trave o JS
                st.markdown(f"""
                    <a href="{row['Link']}" target="_blank" class="backup-link">
                        Se não abrir, clique aqui <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                """, unsafe_allow_html=True)

            # 3. Footer (HTML Bottom)
            st.markdown(f"""
                <div class="card-meta">
                    <small><i class="fa-solid fa-user"></i> {row['Responsavel'].split()[0]}</small>
                    <small><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</small>
                </div>
            </div> <div style="margin-bottom: 25px;"></div>
            """, unsafe_allow_html=True)

# --- ADMIN (LÓGICA APURADA) ---
def render_admin():
    if not st.session_state.admin_logged:
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            st.markdown("### Login Administrativo")
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

    # Sidebar Admin
    with st.sidebar:
        st.success("Administrador Logado")
        if st.button("Sair"):
            st.session_state.admin_logged = False
            st.session_state.view = 'landing'
            st.rerun()

    render_header("Analytics & Monitoramento", "Análise de engajamento do catálogo de dados.")

    # Verifica Logs
    if not os.path.exists(LOG_FILE):
        st.info("Aguardando dados de acesso. O arquivo de log será criado automaticamente.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            st.warning("Arquivo de log existe mas está vazio.")
            return

        # Processamento de Dados (Métricas Inteligentes)
        df['Data'] = pd.to_datetime(df['Data'])
        total_clicks = len(df)
        
        # 1. Crescimento (Hoje vs Média Diária)
        hoje = pd.Timestamp.now().normalize()
        clicks_hoje = len(df[df['Data'] >= hoje])
        
        # 2. Horário de Pico (Moda da coluna Hora)
        pico_hora = int(df['Hora'].mode()[0])
        pico_fmt = f"{pico_hora}h - {pico_hora+1}h"
        
        # 3. Dashboard + Popular
        top_dash = df['Dashboard'].mode()[0]
        
        # 4. Departamento + Ativo
        top_dept = df['Departamento'].mode()[0]

        # Renderização KPIs
        k1, k2, k3, k4 = st.columns(4)
        kpi_card("Total de Acessos", total_clicks, "fa-chart-line", None, k1)
        kpi_card("Acessos Hoje", clicks_hoje, "fa-calendar-day", None, k2)
        kpi_card("Horário de Pico", pico_fmt, "fa-clock", None, k3)
        kpi_card("Setor Mais Engajado", top_dept, "fa-users", None, k4)

        st.markdown("---")

        # Gráficos
        col_g1, col_g2 = st.columns([2, 1])
        
        with col_g1:
            st.markdown("#### Evolução Temporal de Acessos")
            # Agrupa por Data (Dia)
            df_time = df.set_index('Data').resample('D').size()
            st.line_chart(df_time, color=THEME['accent'])
            
        with col_g2:
            st.markdown("#### Top Dashboards")
            st.bar_chart(df['Dashboard'].value_counts().head(5), color=THEME['accent'])

        st.markdown("#### Detalhamento dos Logs")
        st.dataframe(
            df.sort_values(by="Data", ascending=False),
            use_container_width=True,
            column_config={
                "Data": st.column_config.DatetimeColumn("Data/Hora", format="DD/MM/YYYY HH:mm")
            }
        )

    except Exception as e:
        st.error(f"Erro ao processar analytics: {e}")

# ==============================================================================
# MAIN LOOP
# ==============================================================================
if st.session_state.view == 'landing': render_landing()
elif st.session_state.view == 'gallery': render_gallery()
elif st.session_state.view == 'admin': render_admin()

st.markdown("---")
st.markdown(f"<div style='text-align:center; font-size:0.8rem; color:{THEME['text_muted']}'>Intelligence Hub v2.1 • Acesso Corporativo</div>", unsafe_allow_html=True)