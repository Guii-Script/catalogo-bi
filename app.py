import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ============================
# CONFIGURACAO DA PAGINA
# ============================
st.set_page_config(
    page_title="Portfolio BI | Intelligence Hub",
    page_icon="chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CONSTANTES E ARQUIVOS
# ============================
BASE_DIR = Path(".")
LOG_FILE = BASE_DIR / "access_log.csv"

# ============================
# SESSION STATE
# ============================
if "authenticated_admin" not in st.session_state:
    st.session_state.authenticated_admin = False

if "selected_publico" not in st.session_state:
    st.session_state.selected_publico = "Todos"

# ============================
# TEMA
# ============================
THEME = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "border": "#334155",
    "accent": "#38bdf8",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "success": "#10b981",
}

# ============================
# CSS GLOBAL
# ============================
def load_css():
    st.markdown(
        f"""
        <style>
        body {{ background-color: {THEME['bg']}; color: {THEME['text']}; }}
        .block-container {{ padding-top: 2rem; }}
        .card {{
            background-color: {THEME['card']};
            border: 1px solid {THEME['border']};
            border-radius: 12px;
            padding: 1.5rem;
            height: 100%;
        }}
        .card-title {{ font-size: 1.1rem; font-weight: 600; }}
        .card-desc {{ font-size: 0.9rem; color: {THEME['muted']}; }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75rem;
            border: 1px solid {THEME['border']};
            margin-right: 6px;
        }}
        .btn-link {{
            display: block;
            text-align: center;
            background-color: {THEME['accent']};
            color: #020617 !important;
            padding: 0.6rem;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

load_css()

# ============================
# DADOS
# ============================
URL_PLANILHA = st.secrets.get("GOOGLE_SHEET_URL")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin")

@st.cache_data(ttl=600)
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    expected = [
        "Nome_Dash", "Descricao", "Link", "Status",
        "Responsavel", "Publico", "Midia",
        "Periodicidade", "Horario", "Divulgacao"
    ]
    for col in expected:
        if col not in df.columns:
            df[col] = "N/A"
    return df.fillna("N/A").astype(str)

if not URL_PLANILHA:
    st.error("Fonte de dados nao configurada")
    st.stop()

df = load_data(URL_PLANILHA)
df_active = df[df["Status"].str.lower() == "ativo"]

# ============================
# LOG DE ACESSO
# ============================
def log_access(dashboard_name: str):
    now = datetime.now()
    entry = pd.DataFrame([
        {
            "dashboard": dashboard_name,
            "date": now.date(),
            "month": now.strftime("%Y-%m"),
            "timestamp": now
        }
    ])

    if LOG_FILE.exists():
        entry.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        entry.to_csv(LOG_FILE, index=False)

# ============================
# SIDEBAR
# ============================
st.sidebar.title("Portfolio BI")

page = st.sidebar.radio(
    "Navegacao",
    ["Catalogo", "Administracao"]
)

# ============================
# CATALOGO PUBLICO
# ============================
if page == "Catalogo":
    st.title("Catalogo de Dashboards")
    st.caption("Central corporativa de indicadores e relatorios")

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        publico_opts = ["Todos"] + sorted(df_active["Publico"].unique())
        publico_sel = st.selectbox("Publico", publico_opts)

    with col_f2:
        resp_sel = st.selectbox("Responsavel", ["Todos"] + sorted(df_active["Responsavel"].unique()))

    with col_f3:
        midia_sel = st.selectbox("Plataforma", ["Todos"] + sorted(df_active["Midia"].unique()))

    search = st.text_input("Buscar dashboard")

    df_show = df_active.copy()

    if publico_sel != "Todos":
        df_show = df_show[df_show["Publico"].str.contains(publico_sel, case=False)]
    if resp_sel != "Todos":
        df_show = df_show[df_show["Responsavel"] == resp_sel]
    if midia_sel != "Todos":
        df_show = df_show[df_show["Midia"] == midia_sel]
    if search:
        df_show = df_show[df_show["Nome_Dash"].str.contains(search, case=False)]

    if df_show.empty:
        st.info("Nenhum dashboard encontrado")
    else:
        cols = st.columns(3)
        for idx, row in enumerate(df_show.to_dict("records")):
            with cols[idx % 3]:
                st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='card-title'>{row['Nome_Dash']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card-desc'>{row['Descricao']}</div>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style='margin:0.5rem 0;'>
                        <span class='badge'>{row['Midia']}</span>
                        <span class='badge'>{row['Periodicidade']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if row["Link"] not in ["N/A", "", "nan"]:
                    if st.button("Acessar", key=f"go_{idx}"):
                        log_access(row["Nome_Dash"])
                        st.markdown(f"<meta http-equiv='refresh' content='0; url={row['Link']}'>", unsafe_allow_html=True)
                else:
                    st.caption("Link indisponivel")

                st.markdown("</div>", unsafe_allow_html=True)

# ============================
# AREA ADMINISTRATIVA
# ============================
if page == "Administracao":
    st.title("Area Administrativa")

    if not st.session_state.authenticated_admin:
        pwd = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.authenticated_admin = True
                st.rerun()
            else:
                st.error("Senha invalida")
    else:
        st.success("Acesso autorizado")

        if not LOG_FILE.exists():
            st.info("Nenhum acesso registrado")
        else:
            log_df = pd.read_csv(LOG_FILE)
            log_df["date"] = pd.to_datetime(log_df["date"])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Acessos Hoje", log_df[log_df["date"] == pd.Timestamp.today().normalize()].shape[0])

            with col2:
                last_7 = pd.Timestamp.today() - pd.Timedelta(days=7)
                st.metric("Ultimos 7 dias", log_df[log_df["date"] >= last_7].shape[0])

            with col3:
                st.metric("Ultimos 30 dias", log_df.shape[0])

            st.subheader("Acessos por Dashboard")
            st.dataframe(log_df["dashboard"].value_counts().reset_index(name="acessos"))
