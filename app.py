import streamlit as st
import pandas as pd
import re
import random # Embora importado, random não está sendo usado. Pode ser removido.

# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed" # Menu começa fechado
)

# --- Paleta de Cores Expandida ---
COLORS = {
    "primary_dark": "#0d2e5b",
    "primary_medium": "#1e4a7f",
    "primary_light": "#5b92c8",
    "accent_purple": "#8B5CF6",
    "accent_teal": "#06D6A0",
    "accent_orange": "#FF9E64",
    "background_main": "#0F172A",
    "background_card": "#1E293B",
    "background_sidebar": "#0F172A",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_accent": "#E2E8F0",
    "white": "#FFFFFF",
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2"
}

# --- CSS Customizado ---
def load_custom_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        
        /* === FUNDO === */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(-45deg, {COLORS['background_main']}, {COLORS['primary_dark']}, {COLORS['background_sidebar']}, {COLORS['primary_medium']});
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: {COLORS['text_primary']};
            font-family: 'Inter', sans-serif;
            position: relative;
            overflow-x: hidden;
        }}
        @keyframes gradientShift {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}

        /* === PARTÍCULAS === */
        [data-testid="stAppViewContainer"]::before {{
            content: ""; position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, {COLORS['primary_light']}aa, transparent 50%),
                radial-gradient(2px 2px at 40px 70px, {COLORS['accent_purple']}aa, transparent 50%),
                radial-gradient(1px 1px at 90px 40px, {COLORS['accent_teal']}aa, transparent 50%),
                radial-gradient(1px 1px at 130px 80px, {COLORS['accent_orange']}aa, transparent 50%);
            background-repeat: repeat; background-size: 250px 250px;
            animation: float 20s linear infinite; z-index: 0; opacity: 0.3;
        }}
        @keyframes float {{ 100% {{ transform: translateY(-250px); }} }}

        /* === HEADER === */
        .main-header {{
            background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem 0; margin-bottom: 3rem;
            position: relative; z-index: 10;
        }}

        /* === TÍTULO PRINCIPAL === */
        h1 {{
            font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 4rem; text-align: center;
            background: linear-gradient(135deg, {COLORS['primary_light']} 0%, {COLORS['accent_purple']} 50%, {COLORS['accent_teal']} 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            margin-bottom: 1rem; position: relative; z-index: 5;
            text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
            animation: titleGlow 3s ease-in-out infinite alternate;
        }}
        @keyframes titleGlow {{
            from {{ text-shadow: 0 4px 20px rgba(139, 92, 246, 0.3); }}
            to {{ text-shadow: 0 4px 30px rgba(6, 214, 160, 0.4), 0 0 40px rgba(91, 146, 200, 0.2); }}
        }}

        /* === SUBTÍTULO === */
        .subtitle-container {{ text-align: center; position: relative; z-index: 5; }}
         .subtitle-container p {{
            color: {COLORS['text_secondary']} !important; font-size: 1.3rem;
            max-width: 700px; margin: 0 auto 3rem auto;
            line-height: 1.6; font-weight: 300;
        }}

        /* === BARRA DE BUSCA === */
        [data-testid="stTextInput"] {{ position: relative; z-index: 10; }}
        [data-testid="stTextInput"] input {{
            background: rgba(30, 41, 59, 0.8) !important; backdrop-filter: blur(10px);
            border: 2px solid rgba(91, 146, 200, 0.3) !important; border-radius: 15px !important;
            color: {COLORS['text_primary']} !important; padding: 1rem 1.5rem !important;
            font-size: 1.1rem !important; transition: all 0.3s ease !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        }}
        [data-testid="stTextInput"] input:focus {{
            border-color: {COLORS['accent_purple']} !important;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.4) !important;
            transform: translateY(-2px);
        }}
        [data-testid="stTextInput"] input::placeholder {{ color: {COLORS['text_secondary']} !important; }}

        /* === SIDEBAR === */
        [data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.95) !important; backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}
        [data-testid="stSidebar"] h2 {{ /* Título "Filtros Avançados" */
            color: {COLORS['text_primary']} !important; font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 1.8rem;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }}
        
        /* === BOTÃO DE RECOLHER/EXPANDIR SIDEBAR === */
        [data-testid="stSidebarNavCollapseButton"] {{
            background-color: rgba(91, 146, 200, 0.2);
            border: 1px solid rgba(91, 146, 200, 0.4); border-radius: 50%;
            transition: all 0.3s ease; transform: scale(1.1);
        }}
        [data-testid="stSidebarNavCollapseButton"]:hover {{
            background-color: rgba(139, 92, 246, 0.3); border-color: rgba(139, 92, 246, 0.5);
            transform: scale(1.2);
        }}
        [data-testid="stSidebarNavCollapseButton"] svg {{ fill: {COLORS['text_primary']}; }}

        /* === CARDS === */
        .portfolio-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 2rem; min-height: 400px;
            display: flex; flex-direction: column; position: relative; overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: cardEntrance 0.8s ease-out forwards; opacity: 0; transform: translateY(50px);
            z-index: 2;
        }}
        @keyframes cardEntrance {{ to {{ opacity: 1; transform: translateY(0); }} }}

        .portfolio-card::before {{ /* Efeito de brilho */
            content: ''; position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.6s;
        }}
        .portfolio-card:hover::before {{ left: 100%; }}

        .portfolio-card:hover {{
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 80px rgba(139, 92, 246, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border-color: rgba(139, 92, 246, 0.3);
        }}
        
        .portfolio-card h2 {{ /* Título do card */
            color: {COLORS['text_accent']}; font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 1.5rem; line-height: 1.3; margin-bottom: 0.5rem;
        }}
        
        .portfolio-card p {{ /* Descrição do card */
             color: {COLORS['text_secondary']}; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;
        }}

        /* === TÍTULOS DAS SEÇÕES === */
        h3 {{
            font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.5rem; text-align: center;
            margin-top: 5rem; margin-bottom: 1rem; padding-bottom: 25px;
            position: relative; color: {COLORS['text_primary']}; z-index: 5;
        }}
        h3::after {{ /* Linha decorativa */
            content: ''; position: absolute; bottom: 0; left: 50%;
            transform: translateX(-50%); width: 100px; height: 4px;
            background: linear-gradient(90deg, {COLORS['accent_purple']}, {COLORS['accent_teal']});
            border-radius: 2px;
        }}

        /* === TAGS === */
        .tag-wrapper {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 1.5rem 0; margin-top: auto; }}
        .tag {{
            background: rgba(139, 92, 246, 0.2); color: {COLORS['text_primary']}; padding: 8px 16px;
            border-radius: 25px; font-weight: 600; font-size: 0.85rem;
            border: 1px solid rgba(139, 92, 246, 0.3); backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        .tag:hover {{ transform: translateY(-2px); background: rgba(139, 92, 246, 0.3); box-shadow: 0 5px 15px rgba(139, 92, 246, 0.2); }}
        .tag.status-ativo {{ background: rgba(6, 214, 160, 0.2); border-color: rgba(6, 214, 160, 0.3); }}
        .tag.status-inativo {{ background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.3); }}

        /* === BOTÕES === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important; border: none !important; border-radius: 12px !important;
            font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.3s ease !important;
            position: relative; overflow: hidden;
            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3) !important; width: 100%;
        }}
        [data-testid="stButton"] button::before, [data-testid="stLinkButton"] a::before {{ /* Efeito de brilho */
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }}
        [data-testid="stButton"] button:hover::before, [data-testid="stLinkButton"] a:hover::before {{ left: 100%; }}
        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-3px) !important; box-shadow: 0 12px 35px rgba(139, 92, 246, 0.5) !important;
        }}
        [data-testid="stButton"] button:disabled {{ /* Botão desabilitado */
            background: rgba(55, 65, 81, 0.5) !important; color: {COLORS['text_secondary']} !important;
            box-shadow: none !important; transform: none !important; opacity: 0.7;
        }}

        /* === POPOVER === */
        [data-testid="stPopover"] {{
            background: rgba(30, 41, 59, 0.95) !important; backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}
        [data-testid="stPopover"] p, [data-testid="stPopover"] span, [data-testid="stPopover"] li {{ color: {COLORS['text_primary']} !important; }}
        [data-testid="stPopover"] strong {{ color: {COLORS['accent_teal']}; }}
        [data-testid="stPopover"] button {{ /* Botão "Detalhes" */
             background: rgba(55, 65, 81, 0.5) !important; color: {COLORS['text_primary']} !important;
             border: 1px solid rgba(255, 255, 255, 0.1) !important; width: 100%;
        }}
        [data-testid="stPopover"] button:hover {{ background: rgba(75, 85, 99, 0.7) !important; border-color: {COLORS['accent_purple']} !important; }}

        /* === ESTATÍSTICAS NO HEADER === */
        .stats-container {{ display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; }}
        .stat-item {{
            text-align: center; background: rgba(30, 41, 59, 0.6); padding: 1.5rem 2rem;
            border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); transition: all 0.3s ease;
        }}
        .stat-item:hover {{ transform: translateY(-5px); border-color: {COLORS['accent_purple']}; box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2); }}
        .stat-number {{
            font-size: 2.5rem; font-weight: 800; display: block;
            background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_teal']});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .stat-label {{ color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; }}

        /* === RESPONSIVIDADE === */
        @media (max-width: 768px) {{ h1 {{ font-size: 2.5rem; }} .stats-container {{ gap: 1rem; }} .stat-item {{ padding: 1rem; }} }}

        /* === SCROLLBAR === */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: {COLORS['background_main']}; }}
        ::-webkit-scrollbar-thumb {{ background: linear-gradient(135deg, {COLORS['primary_light']}, {COLORS['accent_purple']}); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['accent_teal']}); }}
        </style>
    """, unsafe_allow_html=True)

# Executa o CSS
load_custom_css()

# --- Carregamento de Dados ---
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado.")
    st.stop()

@st.cache_data(ttl=600)
def carregar_dados(url):
    try:
        df = pd.read_csv(url, encoding='utf-8')
        colunas_esperadas = ['Nome_Dash','Descricao','Link','Status','Responsavel','Publico','Midia','Periodicidade','Horario','Divulgacao']
        for c in colunas_esperadas:
            if c not in df.columns: df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_PLANILHA)

# --- Header com Estatísticas ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("Portfólio de Business Intelligence")

st.markdown(
    "<div class='subtitle-container'><p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos</p></div>",
    unsafe_allow_html=True,
)


if not df.empty:
    total_dashboards = len(df)
    ativos = len(df[df['Status'].str.lower() == 'ativo'])
    plataformas = df[df['Midia'].str.lower() != 'n/a']['Midia'].nunique()
    
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-item">
                <span class="stat-number">{total_dashboards}</span>
                <span class="stat-label">Dashboards</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{ativos}</span>
                <span class="stat-label">Ativos</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{plataformas}</span>
                <span class="stat-label">Plataformas</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Fecha .main-header

# --- Barra Lateral com Logo e Filtros ---
st.sidebar.image("fundo.png", use_container_width=True) # Adiciona Logo
st.sidebar.markdown("---")
st.sidebar.header("Filtros Avançados")

if not df.empty:
    def lista(col):
        return ["Todos"] + sorted(df[col].replace('N/A', pd.NA).dropna().unique().tolist())

    filtro_responsavel = st.sidebar.selectbox("👤 Responsável", lista("Responsavel"))
    filtro_publico = st.sidebar.selectbox("🎯 Público", lista("Publico"))
    filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista("Midia"))
    filtro_status = st.sidebar.selectbox("📈 Status", lista("Status"))
    
    st.sidebar.markdown("---") # Divisor

    # --- Lógica de Busca e Filtro ---
    search_term = st.text_input("🔍 **Buscar dashboards:**", placeholder="Digite o nome do dashboard, tecnologia ou palavra-chave...")
    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento

    # Aplicar filtros
    df_filtrado = df.copy()
    if search_term:
        df_filtrado = df_filtrado[
            df_filtrado["Nome_Dash"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Descricao"].str.contains(search_term, case=False, na=False) |
            df_filtrado["Midia"].str.contains(search_term, case=False, na=False)
        ]
    
    filter_mapping = {
        "Responsavel": (filtro_responsavel, "Todos"),
        "Publico": (filtro_publico, "Todos"), 
        "Midia": (filtro_midia, "Todos"),
        "Status": (filtro_status, "Todos")
    }
    
    for col, (filtro, padrao) in filter_mapping.items():
        if filtro != padrao:
            df_filtrado = df_filtrado[df_filtrado[col] == filtro]

    # --- Exibição dos Cards em Grid (Com Agrupamento por Público) ---
    if len(df_filtrado) == 0:
        st.error("🔍 Nenhum dashboard encontrado com os critérios selecionados.")
        st.info("💡 Tente ajustar os filtros ou termos de busca.")
    else:
        # Define os grupos de público para iterar
        grupos = [filtro_publico] if filtro_publico != "Todos" else sorted(df_filtrado["Publico"].replace('N/A', pd.NA).dropna().unique())
        
        for g in grupos:
            # Adiciona o título da seção
            st.markdown(f"### {g}") # Removido o emoji
            # Filtra o dataframe para o grupo atual
            subset = df_filtrado[df_filtrado["Publico"] == g]
            
            reports_list = subset.to_dict('records')
            NUM_COLUNAS = 3
                
            for i in range(0, len(reports_list), NUM_COLUNAS):
                cols = st.columns(NUM_COLUNAS)
                chunk = reports_list[i : i + NUM_COLUNAS]

                for j, row in enumerate(chunk):
                    with cols[j]:
                        st.markdown(f'<div class="portfolio-card" style="animation-delay: {j*0.1}s">', unsafe_allow_html=True)
                        
                        platform_icons = {'Power BI': '📊','Tableau': '📈','Qlik': '🔍','Google Data Studio': '🌐','Excel': '📋','Metabase': '🛠️'}
                        icon = platform_icons.get(row['Midia'], '📊')
                        
                        st.subheader(f"{icon} {row['Nome_Dash']}")
                        st.write(row['Descricao'])

                        status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"
                        st.markdown(
                            f"""
                            <div class="tag-wrapper">
                                <span class="tag">🖥️ {row['Midia']}</span>
                                <span class="tag {status_class}">● {row['Status']}</span>
                                <span class="tag">🕐 {row['Periodicidade']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Chave única inclui o grupo 'g'
                        key_base = f"{g}_{i}_{j}" 
                        
                        st.markdown('<div style="margin-top: auto;">', unsafe_allow_html=True) 
                        col_btn1, col_btn2 = st.columns([1, 1])
                        
                        with col_btn1:
                            # Popover SEM key
                            with st.popover("📋 Detalhes"):
                                st.write(f"**👤 Responsável:** {row['Responsavel']}")
                                st.write(f"**🕐 Periodicidade:** {row['Periodicidade']}")
                                st.write(f"**⏰ Horário:** {row['Horario']}")
                                st.write(f"**📢 Divulgação:** {row['Divulgacao']}")
                                st.write(f"**🎯 Público:** {row['Publico']}")
                        
                        with col_btn2:
                            
                            link_value_raw = row.get("Link", "") 
                            
                            
                            link_value = ""
                            
                            if isinstance(link_value_raw, str):
                                link_value = link_value_raw.strip()

                            
                            if link_value and link_value.lower() != "n/a":
                                try: 
                                    st.link_button(
                                        "🚀 Acessar",          
                                        link_value,           
                                        use_container_width=True,
                                        key=f"link_{key_base}" 
                                    )
                                except TypeError as te:
                                     
                                     st.error(f"Link Error: Could not process URL for '{row.get('Nome_Dash', 'N/A')}'")
                                     st.button("Link Inválido", use_container_width=True, disabled=True, key=f"btn_{key_base}_err")
                                except Exception as e: 
                                     st.error(f"Error: {e}")
                                     st.button("Link Inválido", use_container_width=True, disabled=True, key=f"btn_{key_base}_err2")


                            else:
                                
                                st.button("⏳ Em breve", use_container_width=True, disabled=True, key=f"btn_{key_base}")
                        
                        st.markdown('</div>', unsafe_allow_html=True) # Fecha container do rodapé
                        st.markdown('</div>', unsafe_allow_html=True) # Fecha .portfolio-card
                
                # Espaço entre as linhas do grid
                st.markdown("<br>", unsafe_allow_html=True) 
            
            # Espaço extra entre as seções
            st.markdown("<br>", unsafe_allow_html=True) 

else:
    st.warning("📊 Aguardando dados... Verifique a conexão com a planilha.")

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style='color: {COLORS['text_secondary']}; font-size: 0.8rem; text-align: center;'>
        <p>✨ Portfólio BI v2.0</p>
        <p>Dados atualizados a cada 10 minutos</p>
    </div>
    """, 
    unsafe_allow_html=True
)