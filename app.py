import streamlit as st
import pandas as pd


# --- Configuração da Página ---
st.set_page_config(
    page_title="Portfólio BI | Dashboard Gallery",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed" # Menu começa fechado
)

# --- Inicialização do Session State ---
if 'team_selected' not in st.session_state:
    st.session_state.team_selected = False
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = "Todos" # Valor padrão


# --- Paleta de Cores Profissional ---
COLORS = {
    "primary_dark": "#0d2e5b",
    "primary_medium": "#1e4a7f",
    "primary_light": "#5b92c8",
    "accent_purple": "#5b92c8",      # Cor de acento principal (azul)
    "accent_teal": "#06D6A0",        # Usado para status "Ativo"
    "accent_orange": "#5b92c8",      # Cor de acento secundária (azul)
    "background_main": "#0F172A",
    "background_card": "#1E293B",
    "background_sidebar": "#0F172A",
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_accent": "#E2E8F0",
    "white": "#FFFFFF",
    "gradient_start": "#1e4a7f",
    "gradient_end": "#0d2e5b"
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
            color: {COLORS['text_primary']}; 
            margin-bottom: 1rem; position: relative; z-index: 5;
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
            margin-bottom: 2rem;
        }}
        
        /* === BOTÃO DE RECOLHER/EXPANDIR SIDEBAR === */
        [data-testid="stSidebarNavCollapseButton"] {{
            background-color: rgba(91, 146, 200, 0.2);
            border: 1px solid rgba(91, 146, 200, 0.4); border-radius: 50%;
            transition: all 0.3s ease; transform: scale(1.1);
        }}
        [data-testid="stSidebarNavCollapseButton"]:hover {{
            background-color: rgba(91, 146, 200, 0.3);
            border-color: rgba(91, 146, 200, 0.5);
            transform: scale(1.2);
        }}
        [data-testid="stSidebarNavCollapseButton"] svg {{ fill: {COLORS['text_primary']}; }}

        /* === CARDS === */
        .portfolio-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 2rem; 
            min-height: 250px; 
            height: 100%; 
            display: flex; flex-direction: column; position: relative; overflow: hidden;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            animation: cardEntrance 0.8s ease-out forwards; opacity: 0; transform: translateY(50px);
            z-index: 2;
        }}
        @keyframes cardEntrance {{ to {{ opacity: 1; transform: translateY(0); }} }}

        .portfolio-card::before {{ /* Efeito de brilho sutil */
            content: ''; position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
            transition: left 0.6s;
        }}
        .portfolio-card:hover::before {{ left: 100%; }}

        .portfolio-card:hover {{
            transform: translateY(-10px) scale(1.01);
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border-color: {COLORS['accent_purple']};
        }}
        
        [data-testid="stImage"] img {{
             border-radius: 10px !important;
             object-fit: cover;
             max-height: 200px;
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
            background: {COLORS['accent_purple']};
            border-radius: 2px;
        }}

        /* === TAGS === */
        .tag-wrapper {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 1.5rem 0; margin-top: auto; }}
        .tag {{
            background: rgba(91, 146, 200, 0.2); 
            color: {COLORS['text_primary']}; padding: 8px 16px;
            border-radius: 25px; font-weight: 600; font-size: 0.85rem;
            border: 1px solid rgba(91, 146, 200, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}
        .tag:hover {{ 
            transform: translateY(-2px); 
            background: rgba(91, 146, 200, 0.3);
        }}
        .tag.status-ativo {{ background: rgba(6, 214, 160, 0.2); border-color: rgba(6, 214, 160, 0.3); }}
        .tag.status-inativo {{ background: rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.3); }}

        /* === BOTÕES === */
        [data-testid="stButton"] button, [data-testid="stLinkButton"] a {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important; border: none !important; border-radius: 12px !important;
            font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.3s ease !important;
            position: relative; overflow: hidden;
            width: 100%;
            text-decoration: none; display: inline-block; text-align: center; line-height: normal; cursor: pointer;
        }}
        [data-testid="stButton"] button::before, [data-testid="stLinkButton"] a::before {{ /* Efeito de brilho sutil */
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }}
        [data-testid="stButton"] button:hover::before, [data-testid="stLinkButton"] a:hover::before {{ left: 100%; }}
        
        [data-testid="stButton"] button:hover, [data-testid="stLinkButton"] a:hover {{
            transform: translateY(-3px) !important; 
        }}
        [data-testid="stButton"] button:disabled {{ /* Botão desabilitado */
            background: rgba(55, 65, 81, 0.5) !important; color: {COLORS['text_secondary']} !important;
            box-shadow: none !important; transform: none !important; opacity: 0.7; cursor: not-allowed;
        }}

        /* === ESTILO PARA O BOTÃO DE FALLBACK === */
        .fallback-link-button {{
            background: linear-gradient(135deg, {COLORS['accent_purple']}, {COLORS['primary_light']}) !important;
            color: {COLORS['white']} !important; border: none !important; border-radius: 12px !important;
            font-weight: 600 !important; padding: 12px 24px !important; transition: all 0.3s ease !important;
            position: relative; overflow: hidden;
            width: 100%;
            text-decoration: none !important; display: inline-block; text-align: center;
            line-height: normal; cursor: pointer; box-sizing: border-box;
        }}
         .fallback-link-button:hover {{
            transform: translateY(-3px) !important;
            color: {COLORS['white']} !important;
        }}
        .fallback-link-button::before {{
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }}
        .fallback-link-button:hover::before {{ left: 100%; }}

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
        [data-testid="stPopover"] button:hover {{ 
            background: rgba(75, 85, 99, 0.7) !important; 
            border-color: {COLORS['accent_purple']} !important;
        }}

        /* === ESTATÍSTICAS NO HEADER === */
        .stats-container {{ display: flex; justify-content: center; gap: 3rem; margin: 2rem 0; flex-wrap: wrap; }}
        .stat-item {{
            text-align: center; background: rgba(30, 41, 59, 0.6); padding: 1.5rem 2rem;
            border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px); transition: all 0.3s ease;
        }}
        .stat-item:hover {{ 
            transform: translateY(-5px); 
            border-color: {COLORS['accent_purple']};
        }}
        .stat-number {{
            font-size: 2.5rem; font-weight: 800; display: block;
            color: {COLORS['primary_light']};
        }}
        .stat-label {{ color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; }}

        /* === RESPONSIVIDADE === */
        @media (max-width: 768px) {{ h1 {{ font-size: 2.5rem; }} .stats-container {{ gap: 1rem; }} .stat-item {{ padding: 1rem; }} }}

        /* === SCROLLBAR === */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: {COLORS['background_main']}; }}
        ::-webkit-scrollbar-thumb {{ 
            background: {COLORS['primary_medium']}; 
            border-radius: 4px; 
        }}
        ::-webkit-scrollbar-thumb:hover {{ 
            background: {COLORS['primary_light']}; 
        }}
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
        colunas_esperadas = ['Nome_Dash','Descricao', 'Imagem_Path','Link','Status','Responsavel','Publico','Midia','Periodicidade','Horario','Divulgacao']
        for c in colunas_esperadas:
            if c not in df.columns: df[c] = pd.NA
        df.fillna("N/A", inplace=True)
        return df.astype(str)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Carrega o DataFrame COMPLETO para os KPIs
df_full = carregar_dados(URL_PLANILHA)

# Cria um DataFrame filtrado (só ativos) para usar no app (filtros, cards)
if not df_full.empty and 'Status' in df_full.columns:
    df_active = df_full[df_full['Status'].str.lower() == 'ativo'].copy()
else:
    # Garante um df vazio com as colunas certas, se o df_full estiver vazio
    df_active = pd.DataFrame(columns=df_full.columns)


# --- Função Helper ---
# --- MODIFICAÇÃO 1: Função 'lista' atualizada para lidar com 'Publico' ---
def lista(col):
    if df_active.empty:
        return ["Todos"]
    
    # Lógica especial para a coluna "Publico"
    if col == "Publico":
        # 1. Pega todos os valores únicos (ex: "Gerente/Supervisor", "Diretor", "Gerente")
        publico_strings = df_active['Publico'].replace('N/A', pd.NA).dropna().unique()
        
        # 2. Usa um set para armazenar valores individuais (evita duplicatas)
        all_individual_teams = set()

        # 3. Itera, quebra (split) por "/" e adiciona ao set
        for s in publico_strings:
            split_teams = [team.strip() for team in s.split('/')] 
            all_individual_teams.update(split_teams)
        
        # 4. Converte para uma lista ordenada e remove valores vazios
        teams = sorted(list(all_individual_teams))
        teams = [t for t in teams if t and t.lower() not in ["todos", "n/a"]]
        return ["Todos"] + teams
    
    # Comportamento padrão para todas as outras colunas
    return ["Todos"] + sorted(df_active[col].replace('N/A', pd.NA).dropna().unique().tolist())
# --- FIM DA MODIFICAÇÃO 1 ---


# --- "ROTEADOR" PRINCIPAL (Tela de Seleção de Time) ---
if not st.session_state.team_selected:
    
    st.title("Bem-vindo(a) ao Portfólio BI")
    st.markdown(
        "<div class='subtitle-container'><p>Para começar, selecione o seu time para ver os dashboards relevantes.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if not df_active.empty: # Usa df_active para popular os times
        
        # (Não é necessária modificação aqui, pois a 'lista("Publico")' já foi corrigida)
        teams = lista("Publico") 
        teams = [t for t in teams if t.lower() not in ["todos", "n/a"]] 

        if not teams:
            st.warning("Nenhum time (Público) encontrado nos dados. Carregando todos os dashboards.")
            if st.button("Continuar"):
                st.session_state.team_selected = True
                st.session_state.selected_team = "Todos"
                st.rerun()
        else:
            st.markdown("### 🎯 Selecione seu Time:")
            st.markdown("<br>", unsafe_allow_html=True)
            
            num_cols = 3 
            cols = st.columns(num_cols)
            col_index = 0
            
            for team in teams:
                with cols[col_index % num_cols]:
                    if st.button(team, key=f"team_{team}", use_container_width=True):
                        st.session_state.team_selected = True
                        st.session_state.selected_team = team
                        st.rerun()
                col_index += 1
            
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("Ou veja todos os dashboards disponíveis:")
            if st.button("Ver Todos os Dashboards 🚀", key="view_all", use_container_width=False):
                st.session_state.team_selected = True
                st.session_state.selected_team = "Todos"
                st.rerun()
    else:
        st.info("Carregando dados dos times...")

# --- PÁGINA PRINCIPAL DO PORTFÓLIO ---
else:
    # --- Header com Estatísticas ---
    st.title("Portfólio de Business Intelligence")

    st.markdown(
        "<div class='subtitle-container'><p>Descubra insights poderosos através da nossa coleção de dashboards estratégicos</p></div>",
        unsafe_allow_html=True,
    )

    # KPIs usam 'df_full' para mostrar o universo total
    if not df_full.empty:
        total_dashboards = len(df_full) # KPI usa o total (incluindo inativos)
        ativos = len(df_full[df_full['Status'].str.lower() == 'ativo'])
        plataformas = df_full[df_full['Midia'].str.lower() != 'n/a']['Midia'].nunique()
        
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
    try:
        st.sidebar.image("fundo.png", use_container_width=True) # Adiciona Logo
    except Exception:
        st.sidebar.warning("Logo 'fundo.png' não encontrada.")
        
    st.sidebar.markdown("---")
    
    if st.sidebar.button("⬅ Voltar (Trocar Time)", use_container_width=True):
        st.session_state.team_selected = False
        st.session_state.selected_team = "Todos"
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.header("Filtros Avançados")

    # Filtros são baseados apenas em dashboards ativos ('df_active')
    if not df_active.empty: 
        publico_list = lista("Publico")
        try:
            # Tenta encontrar o time selecionado na lista (ex: "Gerente")
            default_index = publico_list.index(st.session_state.selected_team)
        except ValueError:
            # Se não encontrar (ex: "Todos" foi selecionado), usa o index 0
            default_index = 0 
            
        filtro_publico = st.sidebar.selectbox(
            "🎯 Público", 
            publico_list, 
            index=default_index 
        )
        
        filtro_responsavel = st.sidebar.selectbox("👤 Responsável", lista("Responsavel"))
        filtro_midia = st.sidebar.selectbox("🖥️ Plataforma BI", lista("Midia"))
        
        st.sidebar.markdown("---") 

        # --- Lógica de Busca e Filtro ---
        search_term = st.text_input("🔍 **Buscar dashboards:**", placeholder="Digite o nome do dashboard, tecnologia ou palavra-chave...")
        st.markdown("<br>", unsafe_allow_html=True) 

        # Começa a partir dos dashboards ativos
        df_filtrado = df_active.copy()
        
        if search_term:
            df_filtrado = df_filtrado[
                df_filtrado["Nome_Dash"].str.contains(search_term, case=False, na=False) |
                df_filtrado["Descricao"].str.contains(search_term, case=False, na=False) |
                df_filtrado["Midia"].str.contains(search_term, case=False, na=False)
            ]
        
        # --- MODIFICAÇÃO 2: Lógica de Filtro atualizada ---
        
        # Aplicar filtros de Responsavel e Midia (que são de correspondência exata)
        exact_filter_mapping = {
            "Responsavel": (filtro_responsavel, "Todos"),
            "Midia": (filtro_midia, "Todos")
        }
        
        for col, (filtro, padrao) in exact_filter_mapping.items():
            if filtro != padrao:
                df_filtrado = df_filtrado[df_filtrado[col] == filtro]
                
        # Aplicar filtro de Público (que usa 'contains' para correspondência parcial)
        if filtro_publico != "Todos":
            # Isso garante que "Gerente" corresponda a "Gerente" e "Gerente/Supervisor"
            df_filtrado = df_filtrado[df_filtrado["Publico"].str.contains(filtro_publico, case=False, na=False)]
        # --- FIM DA MODIFICAÇÃO 2 ---

        # --- Exibição dos Cards em Grid (Com Agrupamento por Público) ---
        if len(df_filtrado) == 0:
            st.error("🔍 Nenhum dashboard encontrado com os critérios selecionados.")
            st.info("💡 Tente ajustar os filtros ou termos de busca.")
        else:
            
            # --- MODIFICAÇÃO 3: Lógica de Agrupamento atualizada ---
            
            # Se um filtro de público específico foi selecionado (ex: "Gerente"),
            # mostramos todos os resultados sob um único título.
            if filtro_publico != "Todos":
                st.markdown(f"### 🎯 Exibindo resultados para: {filtro_publico}")
                # Criamos uma "tupla" simples para o loop de renderização
                grupos_de_dados = [("Resultados", df_filtrado)] 
            
            # Se "Todos" estiver selecionado, agrupamos pelos valores únicos ORIGINAIS
            else:
                grupos = sorted(df_filtrado["Publico"].replace('N/A', pd.NA).dropna().unique())
                grupos_de_dados = []
                for g in grupos:
                    # Filtro exato aqui para criar os grupos corretos
                    subset = df_filtrado[df_filtrado["Publico"] == g]
                    grupos_de_dados.append((g, subset)) # (Título, DataFrame)
            
            # --- FIM DA MODIFICAÇÃO 3 ---
            
            # Loop de renderização (agora usa 'grupos_de_dados')
            for titulo_grupo, subset in grupos_de_dados:
                
                if subset.empty: # Pula se o grupo estiver vazio
                    continue
                
                # Se o título for "Resultados", o título já foi impresso antes do loop
                if titulo_grupo != "Resultados":
                    st.markdown(f"### {titulo_grupo}") 
                
                reports_list = subset.to_dict('records')
                NUM_COLUNAS = 3
                        
                for i in range(0, len(reports_list), NUM_COLUNAS):
                    cols = st.columns(NUM_COLUNAS)
                    chunk = reports_list[i : i + NUM_COLUNAS]

                    for j, row in enumerate(chunk):
                        with cols[j]:
                            # Inicia o card
                            st.markdown('<div class="portfolio-card">', unsafe_allow_html=True)
                            
                            # --- Imagem ---
                            image_path = row.get("Imagem_Path", "")
                            if image_path and image_path.lower() != 'n/a':
                                try:
                                    st.image(image_path, use_container_width=True)
                                except Exception as img_err:
                                    st.warning(f"⚠️ Imagem não encontrada: {image_path}", icon="🖼️")
                            
                            # --- Conteúdo HTML ---
                            platform_icons = {'Power BI': '📊','Tableau': '📈','Qlik': '🔍','Google Data Studio': '🌐','Excel': '📋','Metabase': '🛠️'}
                            icon = platform_icons.get(row['Midia'], '📊')
                            status_class = "status-ativo" if row["Status"].lower() == "ativo" else "status-inativo"
                            
                            html_content = f"""
                                <h2>{icon} {row['Nome_Dash']}</h2>
                                <p>{row['Descricao']}</p>
                                <div class="tag-wrapper">
                                    <span class="tag">🖥️ {row['Midia']}</span>
                                    <span class="tag {status_class}">● {row['Status']}</span>
                                    <span class="tag">🕐 {row['Periodicidade']}</span>
                                </div>
                            """
                            st.markdown(html_content, unsafe_allow_html=True)

                            # --- Botões Nativos ---
                            key_base = f"{titulo_grupo}_{i}_{j}" 
                            
                            col_btn1, col_btn2 = st.columns([1, 1])
                            
                            with col_btn1:
                                with st.popover("📋 Detalhes"):
                                    st.write(f"**👤 Responsável:** {row['Responsavel']}")
                                    st.write(f"**🕐 Periodicidade:** {row['Periodicidade']}")
                                    st.write(f"**⏰ Horário:** {row['Horario']}")
                                    st.write(f"**📢 Divulgação:** {row['Divulgacao']}")
                                    st.write(f"**🎯 Público:** {row['Publico']}")
                            
                            with col_btn2:
                                link_value_raw = row.get("Link", "") 
                                link_value = link_value_raw.strip() if isinstance(link_value_raw, str) else "" 

                                if link_value and link_value.lower() != "n/a":
                                    try: 
                                        st.link_button(
                                            "🚀 Acessar",
                                            link_value,
                                            use_container_width=True,
                                            key=f"link_{key_base}" 
                                        )
                                    except (TypeError, Exception) as e: 
                                        # Fallback para links que falham no st.link_button
                                        fallback_button_html = f"""<a href="{link_value}" target="_blank" class="fallback-link-button" style="text-decoration: none;" title="Abrir link para {row.get('Nome_Dash', 'N/A')}">🚀 Acessar</a>"""
                                        st.markdown(fallback_button_html, unsafe_allow_html=True)
                                else:
                                    st.button("⏳ Em breve", use_container_width=True, disabled=True, key=f"btn_{key_base}")
                            
                            # Fecha o card
                            st.markdown('</div>', unsafe_allow_html=True)
                    
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