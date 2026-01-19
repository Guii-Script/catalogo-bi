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

# Inicialização de estado
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'admin_logged' not in st.session_state:
    st.session_state.admin_logged = False

# ==============================================================================
# SISTEMA DE LOGS
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
        except Exception:
            pass
    return pd.DataFrame(columns=["Data", "Dashboard", "Usuario", "Departamento", "Hora"])

def open_url_in_new_tab(url):
    js = f"<script>window.open('{url}', '_blank').focus();</script>"
    components.html(js, height=0, width=0)

# ==============================================================================
# ESTILIZAÇÃO CSS (REFINADA)
# ==============================================================================
def load_css():
    theme = {
        "bg_main": "#0f172a",
        "bg_card": "#1e293b",
        "border": "#334155",
        "accent": "#0ea5e9",
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
        
        /* Correção de Navegação (Radio fica parecendo menu) */
        .stRadio > div {{ gap: 1rem; }}
        .stRadio label {{ cursor: pointer; font-size: 1rem; padding: 0.5rem; border-radius: 5px; transition: background 0.3s; }}
        .stRadio label:hover {{ background: rgba(255,255,255,0.05); }}
        
        /* Títulos */
        .hero-container {{
            text-align: center; padding: 3rem 1rem;
            background: radial-gradient(circle at center, rgba(14, 165, 233, 0.1) 0%, transparent 70%);
            border-bottom: 1px solid {theme['border']};
            margin-bottom: 2rem;
        }}
        
        /* Cards */
        .card-container {{
            background-color: {theme['bg_card']};
            border: 1px solid {theme['border']};
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.2s ease-in-out;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .card-container:hover {{ border-color: {theme['accent']}; transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3); }}
        
        .card-header {{ padding: 1rem; background-color: rgba(30, 41, 59, 0.8); border-bottom: 1px solid {theme['border']}; }}
        .card-body {{ padding: 1rem; flex-grow: 1; }}
        .card-footer {{ padding: 0.8rem 1rem; background-color: rgba(15, 23, 42, 0.4); border-top: 1px solid {theme['border']}; }}
        
        /* Badges */
        .tech-badge {{
            display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.2rem 0.6rem;
            border-radius: 4px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
            background: rgba(14, 165, 233, 0.1); color: {theme['accent']}; border: 1px solid rgba(14, 165, 233, 0.2);
        }}
        .badge-success {{ background: rgba(16, 185, 129, 0.1); color: #10b981; border-color: rgba(16, 185, 129, 0.2); }}

        /* KPIs */
        .kpi-box {{ background: {theme['bg_card']}; border: 1px solid {theme['border']}; padding: 1.2rem; border-radius: 8px; text-align: center; }}
        .kpi-val {{ font-size: 1.8rem; font-weight: 700; color: {theme['text_head']}; margin: 0.5rem 0; }}
        
        /* CORREÇÃO DO BOTÃO (Texto Apagado) */
        div.stButton > button {{
            width: 100%;
            background-color: {theme['accent']} !important;
            color: #ffffff !important; /* Branco forçado */
            border: none;
            padding: 0.6rem;
            font-weight: 600 !important; /* Mais negrito */
            letter-spacing: 0.5px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2); /* Sombra leve para contraste */
            border-radius: 6px;
            transition: all 0.2s;
        }}
        div.stButton > button:hover {{
            background-color: #0284c7 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
            transform: translateY(-1px);
        }}
        div.stButton > button:active {{ transform: translateY(1px); }}
        
        /* Botão Desabilitado */
        div.stButton > button:disabled {{
            background-color: #334155 !important;
            color: #94a3b8 !important;
            cursor: not-allowed;
            box-shadow: none;
        }}

        .admin-login {{ max-width: 400px; margin: 5rem auto; padding: 2rem; background: {theme['bg_card']}; border: 1px solid {theme['border']}; border-radius: 12px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ==============================================================================
# DADOS
# ==============================================================================
def get_mock_data():
    return pd.DataFrame({
        'Nome_Dash': ['Vendas Global', 'RH Analytics', 'Logística Real-Time', 'Finanças FY24', 'Marketing Digital', 'Controle de Estoque', 'NPS Clientes', 'Produção Fabril'],
        'Descricao': [
            'Acompanhamento de vendas por região e produto com análise YoY.',
            'Headcount, turnover e métricas de desempenho de colaboradores.',
            'Rastreamento de frota e status de entregas em tempo real.',
            'DRE, Fluxo de Caixa e indicadores de rentabilidade.',
            'Performance de campanhas, ROI e análise de leads.',
            'Giro de estoque, curva ABC e previsão de demanda.',
            'Satisfação do cliente e análise de churn rate.',
            'OEE, paradas de linha e eficiência produtiva.'
        ],
        'Link': ['https://google.com'] * 8,
        'Status': ['Ativo', 'Ativo', 'Em Manutenção', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
        'Publico': ['Comercial', 'RH', 'Operações', 'Diretoria', 'Marketing', 'Logística', 'CS', 'Industrial'],
        'Midia': ['PowerBI', 'Tableau', 'PowerBI', 'Excel', 'Google Data Studio', 'Qlik', 'Salesforce', 'PowerBI'],
        'Responsavel': ['Ana Silva', 'Carlos Souza', 'Mariana Lima', 'Roberto Alves', 'Julia Costa', 'Pedro Santos', 'Amanda Lee', 'Ricardo O.'],
        'Periodicidade': ['Diária', 'Mensal', 'Em Tempo Real', 'Mensal', 'Semanal', 'Diária', 'Semanal', 'Real Time']
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
# COMPONENTES
# ==============================================================================
def render_kpi_card(label, value, icon, color="#0ea5e9"):
    return f"""
    <div class="kpi-box">
        <i class="fa-solid {icon}" style="font-size: 1.5rem; color: {color}; margin-bottom: 8px;"></i>
        <div class="kpi-val">{value}</div>
        <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; letter-spacing: 1px;">{label}</div>
    </div>
    """

def render_dashboard_card_interactive(row, compact=False):
    icon_map = {'powerbi': 'fa-chart-bar', 'tableau': 'fa-chart-pie', 'excel': 'fa-file-excel', 'google': 'fa-chart-line'}
    midia = row['Midia'].lower()
    icon = next((v for k, v in icon_map.items() if k in midia), 'fa-chart-simple')
    
    desc_style = "min-height: 2.5em;" if compact else "min-height: 4.5em;"
    
    st.markdown(f"""
    <div class="card-container">
        <div class="card-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; font-size: 1rem; color: #f1f5f9;">{row['Nome_Dash']}</h4>
                <i class="fa-solid {icon}" style="color: #0ea5e9;"></i>
            </div>
        </div>
        <div class="card-body">
            <p style="font-size: 0.85rem; margin: 0; {desc_style} overflow: hidden; color: #94a3b8;">
                {row['Descricao'][:90] + '...' if len(row['Descricao']) > 90 else row['Descricao']}
            </p>
            <div style="margin-top: 10px; display: flex; gap: 5px;">
                <span class="tech-badge">{row['Midia']}</span>
                <span class="tech-badge" style="border-color: rgba(16, 185, 129, 0.2); color: #10b981;">{row['Periodicidade']}</span>
            </div>
        </div>
        <div class="card-footer">
    """, unsafe_allow_html=True)
    
    # Botão Interativo
    btn_key = f"btn_{'home' if compact else 'cat'}_{row['Nome_Dash']}"
    if row['Link'] not in ["N/A", "", "None"]:
        if st.button("Acessar Agora", key=btn_key, use_container_width=True):
            log_access(row['Nome_Dash'], area=row['Publico'])
            open_url_in_new_tab(row['Link'])
    else:
        st.button("Indisponível", disabled=True, key=f"dis_{btn_key}", use_container_width=True)
        
    st.markdown("</div></div><div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# PÁGINAS E NAVEGAÇÃO
# ==============================================================================
def render_sidebar():
    st.sidebar.markdown('<div style="text-align: center; margin-bottom: 2rem;"><i class="fa-solid fa-layer-group" style="font-size: 3rem; color: #0ea5e9;"></i><h2 style="font-size: 1.2rem; margin-top: 10px;">Hub Corporativo</h2></div>', unsafe_allow_html=True)
    
    # Navegação Simplificada (Evita travamentos)
    # Usamos o valor retornado diretamente para controlar a página
    nav_options = ["Lobby Principal", "Catálogo", "Administração"]
    icons = {"Lobby Principal": "🏠", "Catálogo": "📂", "Administração": "⚙️"}
    
    selection = st.sidebar.radio(
        "Menu", 
        nav_options,
        format_func=lambda x: f"{icons[x]}  {x}",
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Filtros só aparecem no catálogo
    filters = None
    if selection == "Catálogo":
        st.sidebar.markdown('<div style="color: #0ea5e9; font-weight: 600; font-size: 0.8rem; margin-bottom: 15px;">FILTRAR RESULTADOS</div>', unsafe_allow_html=True)
        with st.sidebar.container():
            f1 = st.selectbox("Área / Público", ["Todos"] + sorted(df_active['Publico'].unique()))
            f2 = st.selectbox("Tecnologia", ["Todos"] + sorted(df_active['Midia'].unique()))
            filters = (f1, f2)
            st.sidebar.caption(f"{len(df_active)} dashboards disponíveis")
            
    return selection, filters

def page_home():
    st.markdown("""
    <div class="hero-container">
        <h1 style="margin-bottom: 0.5rem;">Bem-vindo ao Intelligence Hub</h1>
        <p style="color: #94a3b8;">Central unificada de dados para tomada de decisão estratégica.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. KPIs
    df_logs = load_access_logs()
    acessos_hoje = len(df_logs[df_logs['Data'].dt.date == datetime.now().date()]) if not df_logs.empty else 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(render_kpi_card("Dashboards", len(df_active), "fa-database"), unsafe_allow_html=True)
    c2.markdown(render_kpi_card("Acessos Hoje", acessos_hoje, "fa-users", "#f59e0b"), unsafe_allow_html=True)
    c3.markdown(render_kpi_card("Áreas", df_active['Publico'].nunique(), "fa-building", "#10b981"), unsafe_allow_html=True)
    c4.markdown(render_kpi_card("Plataformas", df_active['Midia'].nunique(), "fa-laptop-code", "#8b5cf6"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Área de Destaques (Preenchendo a Home)
    st.markdown("### 🔥 Destaques da Semana")
    st.markdown("Os relatórios mais acessados e recomendados para você.")
    
    if not df_active.empty:
        # Pega os 3 primeiros (ou aleatórios) para exibir
        destaques = df_active.head(3)
        cols = st.columns(3)
        for idx, (_, row) in enumerate(destaques.iterrows()):
            with cols[idx]:
                render_dashboard_card_interactive(row, compact=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Atalhos Rápidos
    col_cta1, col_cta2 = st.columns([2, 1])
    with col_cta1:
        st.info("💡 **Dica:** Utilize os filtros no menu lateral da página 'Catálogo' para encontrar relatórios específicos por departamento ou tecnologia.")

def page_catalog(filters):
    pub, mid = filters
    st.markdown("### 📂 Catálogo de Dashboards")
    
    c1, c2 = st.columns([3, 1])
    search = c1.text_input("Search", placeholder="Buscar relatório...", label_visibility="collapsed")
    if c2.button("Limpar Busca", use_container_width=True): st.rerun()
    
    # Filtragem
    df_view = df_active.copy()
    if search:
        term = search.lower()
        df_view = df_view[df_view['Nome_Dash'].str.lower().contains(term) | df_view['Descricao'].str.lower().contains(term)]
    if pub != "Todos": df_view = df_view[df_view['Publico'] == pub]
    if mid != "Todos": df_view = df_view[df_view['Midia'] == mid]
    
    if df_view.empty:
        st.warning("Nenhum resultado encontrado.")
        return

    # Grid
    rows = [df_view.iloc[i:i + 3] for i in range(0, len(df_view), 3)]
    for row_data in rows:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(row_data.iterrows()):
            with cols[idx]:
                render_dashboard_card_interactive(row)

def page_admin():
    if not st.session_state.admin_logged:
        st.markdown('<div class="admin-login"><h3 style="text-align:center;">Admin</h3>', unsafe_allow_html=True)
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar", type="primary", use_container_width=True):
            if pwd == st.secrets.get("ADMIN_PASSWORD", "admin"):
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Acesso Negado")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Painel Admin
    c1, c2 = st.columns([5, 1])
    c1.title("📊 Analytics de Acesso")
    if c2.button("Sair", type="secondary"):
        st.session_state.admin_logged = False
        st.rerun()

    df_logs = load_access_logs()
    if df_logs.empty:
        st.info("Sem dados de acesso ainda.")
        return

    # Gráficos Temporais (Diário, Semanal, Mensal)
    st.markdown("#### Evolução de Acessos")
    
    # Preparação dos dados
    df_chart = df_logs.copy()
    df_chart = df_chart.set_index('Data')
    
    tab_d, tab_w, tab_m = st.tabs(["📅 Diário", "🗓️ Semanal", "📆 Mensal"])
    
    with tab_d:
        daily = df_chart.resample('D').count()['Dashboard'].reset_index(name='Acessos')
        chart_d = alt.Chart(daily).mark_line(point=True, color='#0ea5e9').encode(
            x=alt.X('Data:T', title='Data', axis=alt.Axis(format='%d/%m')),
            y='Acessos:Q', tooltip=['Data', 'Acessos']
        ).properties(height=350)
        st.altair_chart(chart_d, use_container_width=True)
        
    with tab_w:
        weekly = df_chart.resample('W').count()['Dashboard'].reset_index(name='Acessos')
        chart_w = alt.Chart(weekly).mark_bar(color='#10b981').encode(
            x=alt.X('Data:T', title='Semana'),
            y='Acessos:Q', tooltip=['Data', 'Acessos']
        ).properties(height=350)
        st.altair_chart(chart_w, use_container_width=True)
        
    with tab_m:
        monthly = df_chart.resample('M').count()['Dashboard'].reset_index(name='Acessos')
        chart_m = alt.Chart(monthly).mark_bar(color='#8b5cf6').encode(
            x=alt.X('Data:T', title='Mês', axis=alt.Axis(format='%b/%Y')),
            y='Acessos:Q', tooltip=['Data', 'Acessos']
        ).properties(height=350)
        st.altair_chart(chart_m, use_container_width=True)

    # Detalhamento
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Top Dashboards")
        top_dash = df_logs['Dashboard'].value_counts().reset_index()
        top_dash.columns = ['Nome', 'Acessos']
        st.dataframe(top_dash, height=300, use_container_width=True, hide_index=True)
    
    with c2:
        st.markdown("#### Acessos por Hora")
        hourly = df_logs['Hora'].str[:2].value_counts().reset_index()
        hourly.columns = ['Hora', 'Acessos']
        chart_h = alt.Chart(hourly).mark_bar(color='#f59e0b').encode(
            x=alt.X('Hora:N', sort=sorted(hourly['Hora'].unique())), y='Acessos:Q'
        ).properties(height=300)
        st.altair_chart(chart_h, use_container_width=True)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    selection, filters = render_sidebar()
    
    if selection == "Lobby Principal":
        page_home()
    elif selection == "Catálogo":
        page_catalog(filters)
    elif selection == "Administração":
        page_admin()

if __name__ == "__main__":
    main()