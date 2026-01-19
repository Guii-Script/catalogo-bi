import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================================================================
# 1. CONFIGURAÇÃO INICIAL E CONSTANTES
# ==============================================================================
st.set_page_config(
    page_title="Intelligence Hub | BI Corporativo",
    page_icon="static/favicon.png", # Sugestão: usar um arquivo .png real se possível
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tema de Cores Profissional (Dark Slate & Cyan)
THEME = {
    "bg_body": "#0f172a",       # Slate 900
    "bg_card": "#1e293b",       # Slate 800
    "border": "#334155",        # Slate 700
    "accent": "#0ea5e9",        # Sky 500
    "text_main": "#f8fafc",     # Slate 50
    "text_muted": "#94a3b8",    # Slate 400
    "success": "#10b981",       # Emerald 500
    "danger": "#ef4444",        # Red 500
    "gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
}

# Senha de Acesso Admin (Idealmente viria de st.secrets)
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASS", "admin123")

# ==============================================================================
# 2. ESTILIZAÇÃO (CSS AVANÇADO)
# ==============================================================================
def load_custom_css():
    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Global */
        .stApp {{
            background-color: {THEME['bg_body']};
            font-family: 'Inter', sans-serif;
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {THEME['text_main']} !important;
            font-weight: 600;
        }}
        
        /* KPI Cards */
        .kpi-container {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            transition: all 0.3s ease;
        }}
        .kpi-container:hover {{
            border-color: {THEME['accent']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
        }}
        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {THEME['text_main']};
        }}
        .kpi-label {{
            font-size: 0.85rem;
            color: {THEME['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 5px;
        }}
        
        /* Dashboard Cards (Grid System) */
        .dash-card {{
            background-color: {THEME['bg_card']};
            border: 1px solid {THEME['border']};
            border-radius: 10px;
            padding: 0;
            margin-bottom: 20px;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: border 0.3s ease;
        }}
        .dash-card:hover {{
            border-color: {THEME['accent']};
        }}
        
        .card-header {{
            padding: 20px;
            border-bottom: 1px solid {THEME['border']};
            background: linear-gradient(to right, rgba(15, 23, 42, 0.5), transparent);
        }}
        
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {THEME['text_main']};
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .card-body {{
            padding: 20px;
            flex-grow: 1;
            color: {THEME['text_muted']};
            font-size: 0.9rem;
        }}
        
        .card-footer {{
            padding: 15px 20px;
            background-color: rgba(0,0,0,0.2);
            border-top: 1px solid {THEME['border']};
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        /* Badges e Tags */
        .tech-badge {{
            background-color: rgba(14, 165, 233, 0.1);
            color: {THEME['accent']};
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(14, 165, 233, 0.2);
        }}
        
        /* Botão Customizado */
        .btn-access {{
            background-color: {THEME['accent']};
            color: white !important;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            transition: background 0.2s;
            display: inline-block;
        }}
        .btn-access:hover {{
            background-color: #0284c7; /* Sky 600 */
        }}
        .btn-disabled {{
            background-color: {THEME['border']};
            color: {THEME['text_muted']} !important;
            cursor: not-allowed;
            pointer-events: none;
        }}
        
        /* Inputs do Streamlit */
        div[data-baseweb="input"] > div {{
            background-color: {THEME['bg_card']};
            border-color: {THEME['border']};
            color: white;
        }}
        
        /* Landing Page Grid */
        .landing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }}
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

# ==============================================================================
# 3. GERENCIAMENTO DE DADOS E ESTADO
# ==============================================================================

# Inicialização do Session State
if 'view' not in st.session_state:
    st.session_state.view = 'landing'  # Options: landing, gallery, admin
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = "Todos"
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

@st.cache_data(ttl=600)
def get_data():
    try:
        # Tenta pegar dos secrets ou usa um placeholder para teste se falhar
        url = st.secrets.get("GOOGLE_SHEET_URL")
        if not url:
            # Dados Mockados caso não tenha secrets configurado (para testar o layout)
            return pd.DataFrame({
                'Nome_Dash': ['Vendas Gerais', 'Logística SP', 'RH Analytics', 'Financeiro Q1'],
                'Descricao': ['Análise de sell-out e performance mensal', 'Tracking de entregas e frota', 'Headcount e turnover', 'DRE e fluxo de caixa'],
                'Link': ['https://google.com', 'https://google.com', '', 'https://google.com'],
                'Status': ['Ativo', 'Ativo', 'Manutenção', 'Ativo'],
                'Responsavel': ['João Silva', 'Maria B.', 'Carlos T.', 'Ana L.'],
                'Publico': ['Comercial', 'Operações', 'RH', 'Financeiro'],
                'Midia': ['Power BI', 'Excel', 'Looker', 'Power BI'],
                'Periodicidade': ['Diário', 'Tempo Real', 'Mensal', 'Semanal'],
                'Horario': ['08:00', 'Live', 'Dia 05', 'Segunda'],
                'Divulgacao': ['E-mail', 'Link', 'Teams', 'Sharepoint']
            })
            
        df = pd.read_csv(url)
        df.fillna("N/A", inplace=True)
        return df
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return pd.DataFrame()

df_full = get_data()
df_active = df_full[df_full['Status'].str.lower() != 'inativo'].copy() if not df_full.empty else pd.DataFrame()

# ==============================================================================
# 4. COMPONENTES VISUAIS (FUNÇÕES AUXILIARES)
# ==============================================================================
def render_header(title, subtitle):
    st.markdown(f"""
        <div style="margin-bottom: 3rem; text-align: left; border-bottom: 1px solid {THEME['border']}; padding-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">{title}</h1>
            <p style="color: {THEME['text_muted']}; font-size: 1.1rem; margin: 0;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def card_kpi(icon, value, label, col):
    with col:
        st.markdown(f"""
            <div class="kpi-container">
                <div style="font-size: 1.5rem; color: {THEME['accent']}; margin-bottom: 10px;">
                    <i class="fa-solid {icon}"></i>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 5. VIEW: LANDING PAGE (SELEÇÃO DE SETOR)
# ==============================================================================
def render_landing():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Hero Section
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 4rem; color: {THEME['accent']}; margin-bottom: 1rem;">
                    <i class="fa-solid fa-network-wired"></i>
                </div>
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">Intelligence Hub</h1>
                <p style="color: {THEME['text_muted']}; font-size: 1.2rem; line-height: 1.6;">
                    Portal centralizado de acesso aos dashboards estratégicos e operacionais.<br>
                    Selecione sua vertical para iniciar.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Botões de Setor
    if not df_active.empty:
        # Tratamento para separar públicos múltiplos (ex: "RH / Financeiro")
        raw_publicos = df_active['Publico'].unique()
        setores = set()
        for p in raw_publicos:
            parts = [x.strip() for x in str(p).split('/')]
            setores.update(parts)
        
        lista_setores = sorted(list(setores))
        if "N/A" in lista_setores: lista_setores.remove("N/A")
        
        cols_per_row = 4
        # Cria container CSS Grid manual para os botões
        st.markdown('<div class="landing-grid">', unsafe_allow_html=True)
        
        grid_cols = st.columns(cols_per_row)
        for i, setor in enumerate(lista_setores):
            with grid_cols[i % cols_per_row]:
                if st.button(f"{setor}", key=f"btn_{setor}", use_container_width=True):
                    st.session_state.selected_filter = setor
                    st.session_state.view = 'gallery'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Rodapé Landing
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Explorar Catálogo Completo", use_container_width=True):
            st.session_state.selected_filter = "Todos"
            st.session_state.view = 'gallery'
            st.rerun()
    with col_b:
        if st.button("Área Administrativa (Restrito)", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()

# ==============================================================================
# 6. VIEW: GALERIA DE DASHBOARDS
# ==============================================================================
def render_gallery():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown(f"### <i class='fa-solid fa-bars'></i> Menu", unsafe_allow_html=True)
        if st.button("Início", use_container_width=True):
            st.session_state.view = 'landing'
            st.rerun()
        if st.button("Admin", use_container_width=True):
            st.session_state.view = 'admin'
            st.rerun()
            
        st.markdown("---")
        st.markdown("### Filtros")
        
        # Filtro de Público
        raw_publicos = sorted(list(set([x.strip() for item in df_active['Publico'].unique() for x in str(item).split('/')])))
        opts_publico = ["Todos"] + [x for x in raw_publicos if x != "N/A"]
        
        # Sincroniza selectbox com session state
        idx = opts_publico.index(st.session_state.selected_filter) if st.session_state.selected_filter in opts_publico else 0
        selected_pub = st.selectbox("Departamento", opts_publico, index=idx)
        st.session_state.selected_filter = selected_pub
        
        selected_tech = st.multiselect("Tecnologia", df_active['Midia'].unique())
        
        st.markdown("---")
        st.info("ℹ️ Dados atualizados em tempo real via Google Sheets API.")

    # --- Main Content ---
    render_header("Catálogo de Dashboards", f"Visualizando indicadores para: <span style='color:{THEME['accent']}'>{st.session_state.selected_filter}</span>")

    # KPIs Superiores
    k1, k2, k3, k4 = st.columns(4)
    card_kpi("fa-database", len(df_full), "Total Dashboards", k1)
    card_kpi("fa-check-circle", len(df_active), "Ativos", k2)
    card_kpi("fa-users", df_active['Responsavel'].nunique(), "Analistas", k3)
    card_kpi("fa-server", df_active['Midia'].nunique(), "Plataformas", k4)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Barra de Pesquisa
    search = st.text_input("Buscar relatório...", placeholder="Digite o nome, KPI ou descrição...", label_visibility="collapsed")
    
    # Filtragem Lógica
    df_show = df_active.copy()
    
    if st.session_state.selected_filter != "Todos":
        df_show = df_show[df_show['Publico'].str.contains(st.session_state.selected_filter, na=False)]
    
    if selected_tech:
        df_show = df_show[df_show['Midia'].isin(selected_tech)]
        
    if search:
        s = search.lower()
        df_show = df_show[
            df_show['Nome_Dash'].str.lower().str.contains(s) | 
            df_show['Descricao'].str.lower().str.contains(s)
        ]

    # Renderização dos Cards
    if df_show.empty:
        st.warning("Nenhum dashboard encontrado com os filtros atuais.")
    else:
        # Agrupamento visual (Opcional, aqui mostro lista plana em Grid)
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, row in enumerate(df_show.to_dict('records')):
            with cols[i % 3]:
                # Definição de Ícones e Cores por Mídia
                midia_lower = str(row['Midia']).lower()
                icon = "fa-chart-pie"
                if "power" in midia_lower: icon = "fa-chart-bar"
                elif "excel" in midia_lower: icon = "fa-file-excel"
                elif "looker" in midia_lower: icon = "fa-magnifying-glass-chart"
                
                # HTML do Card
                link_html = ""
                if row['Link'] and str(row['Link']).lower() not in ['nan', 'n/a', '']:
                    link_html = f'<a href="{row["Link"]}" target="_blank" class="btn-access btn-access">Acessar <i class="fa-solid fa-arrow-up-right-from-square"></i></a>'
                else:
                    link_html = f'<a class="btn-access btn-disabled">Indisponível</a>'

                st.markdown(f"""
                <div class="dash-card">
                    <div class="card-header">
                        <div class="card-title">
                            <i class="fa-solid {icon}" style="color: {THEME['accent']}"></i>
                            {row['Nome_Dash']}
                        </div>
                    </div>
                    <div class="card-body">
                        <p style="margin-bottom: 10px;">{row['Descricao']}</p>
                        <div style="margin-top: auto;">
                            <span class="tech-badge">{row['Midia']}</span>
                            <span class="tech-badge" style="border-color: {THEME['border']}; color: {THEME['text_muted']};"><i class="fa-regular fa-clock"></i> {row['Periodicidade']}</span>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div style="font-size: 0.8rem; color: {THEME['text_muted']};">
                            <i class="fa-solid fa-user-tie"></i> {row['Responsavel'].split(' ')[0]}
                        </div>
                        {link_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: ADMIN & ANALYTICS
# ==============================================================================
def render_admin():
    # Login Simples
    if not st.session_state.admin_logged:
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            st.markdown(f"<h2 style='text-align:center;'>Acesso Restrito</h2>", unsafe_allow_html=True)
            password = st.text_input("Senha Administrativa", type="password")
            if st.button("Entrar", use_container_width=True):
                if password == ADMIN_PASSWORD:
                    st.session_state.admin_logged = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
            
            if st.button("Voltar", use_container_width=True):
                st.session_state.view = 'landing'
                st.rerun()
        return

    # Painel Admin Logado
    with st.sidebar:
        st.markdown("### Admin Menu")
        if st.button("Sair / Logout", use_container_width=True):
            st.session_state.admin_logged = False
            st.session_state.view = 'landing'
            st.rerun()

    render_header("Área Administrativa", "Monitoramento de uso e engajamento da plataforma")

    # --- SIMULAÇÃO DE DADOS DE ANALYTICS ---
    # Como o Streamlit não rastreia cliques externos nativamente, geramos dados mockados
    # para demonstrar a visão que o time de BI teria.
    
    dates = pd.date_range(end=datetime.today(), periods=30)
    data_mock = []
    dashboards_list = df_active['Nome_Dash'].unique() if not df_active.empty else ['Dash Demo']
    
    for date in dates:
        # Gera acessos aleatórios por dia
        daily_access = np.random.randint(10, 50)
        for _ in range(daily_access):
            data_mock.append({
                'Data': date,
                'Dashboard': np.random.choice(dashboards_list),
                'Usuario': f"User_{np.random.randint(100, 999)}",
                'Departamento': np.random.choice(['RH', 'Financeiro', 'Comercial', 'Logística'])
            })
    
    df_analytics = pd.DataFrame(data_mock)

    # Tabs de Visão
    tab1, tab2 = st.tabs(["📊 Visão Geral de Acessos", "📋 Logs Detalhados"])

    with tab1:
        # Métricas de Tempo
        total_mes = len(df_analytics)
        total_semana = len(df_analytics[df_analytics['Data'] > (datetime.today() - timedelta(days=7))])
        media_dia = int(total_mes / 30)

        c1, c2, c3 = st.columns(3)
        card_kpi("fa-calendar-day", media_dia, "Acessos Médios / Dia", c1)
        card_kpi("fa-calendar-week", total_semana, "Acessos (Últimos 7 dias)", c2)
        card_kpi("fa-calendar", total_mes, "Acessos (Últimos 30 dias)", c3)

        st.markdown("### Tendência de Acessos")
        chart_data = df_analytics.groupby('Data').size()
        st.line_chart(chart_data, color=THEME['accent'])

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### Top 5 Dashboards Mais Acessados")
            top_dash = df_analytics['Dashboard'].value_counts().head(5)
            st.bar_chart(top_dash, color=THEME['success'])
        
        with col_b:
            st.markdown("### Engajamento por Departamento")
            dept_chart = df_analytics['Departamento'].value_counts()
            st.bar_chart(dept_chart, color=THEME['text_muted'])

    with tab2:
        st.markdown("### Log de Atividade Recente")
        st.dataframe(
            df_analytics.sort_values(by='Data', ascending=False),
            use_container_width=True,
            hide_index=True
        )

# ==============================================================================
# 8. ROTEADOR DE PÁGINAS (MAIN LOOP)
# ==============================================================================
if st.session_state.view == 'landing':
    render_landing()
elif st.session_state.view == 'gallery':
    render_gallery()
elif st.session_state.view == 'admin':
    render_admin()

# Rodapé Global
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: {THEME['text_muted']}; font-size: 0.8rem;'>"
    f"© {datetime.now().year} Intelligence Hub • Desenvolvido pela Equipe de BI"
    "</div>", 
    unsafe_allow_html=True
)