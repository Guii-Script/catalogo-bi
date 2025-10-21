import streamlit as st
import pandas as pd

# Define as configurações da página (título da aba, ícone e layout)
# 'layout="wide"' usa o espaço total da tela.
st.set_page_config(
    page_title="Portfólio de BI",
    page_icon="💼",
    layout="wide"
)

# --- Injeção de CSS ---
# Esta função injeta nosso CSS customizado para os cards
def load_custom_css():
    st.markdown("""
        <style>
            /* Define um fundo levemente cinza para a aplicação */
            [data-testid="stAppViewContainer"] {
                background-color: #F0F2F6;
            }

            /* Este é o "card" 
            Alvo: O container que o Streamlit cria com 'border=True' 
            */
            [data-testid="stVerticalBlockBorderWrapper"] > div {
                background-color: #FFFFFF;         /* Fundo branco para o card */
                border-radius: 10px;               /* Cantos arredondados */
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* Sombra profissional */
                transition: transform 0.2s ease-in-out; /* Animação no hover */
                min-height: 360px;                 /* Altura mínima para alinhar o grid */
                display: flex;                     /* Ativa o Flexbox */
                flex-direction: column;            /* Organiza o conteúdo em coluna */
                padding: 20px 20px 15px 20px;      /* Espaçamento interno */
            }

            /* Efeito de "zoom" ao passar o mouse */
            [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
                transform: scale(1.02);
            }
            
            /* Este é o "truque" do layout.
            Força os botões (stButton, stLinkButton) a irem para o fundo do card.
            'margin-top: auto' preenche o espaço vazio acima do botão.
            */
            .stButton, .stLinkButton {
                margin-top: auto;
            }
            
            /* Customiza o popover (detalhes) */
            [data-testid="stPopover"] {
                background-color: #FFFFFF;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

# Executa a função para carregar o CSS
load_custom_css()


# --- Carregamento de Dados ---

# Busca a URL da planilha dos 'Secrets' do Streamlit.
# Isso é vital para a segurança, mantendo o link fora do código público.
try:
    URL_PLANILHA = st.secrets["GOOGLE_SHEET_URL"]
except KeyError:
    st.error("Erro de Configuração: O 'GOOGLE_SHEET_URL' não foi configurado nos Secrets deste app.")
    st.info("Por favor, vá em 'Settings' > 'Secrets' no painel do Streamlit e adicione o link da sua planilha.")
    st.stop()
except Exception as e:
    st.error(f"Um erro inesperado ocorreu ao tentar ler os segredos: {e}")
    st.stop()


# Função para carregar e cachear os dados da planilha.
# O cache (ttl=600) salva os dados por 10 minutos, evitando
# recarregar do Google Sheets a cada clique e melhorando a performance.
@st.cache_data(ttl=600)
def carregar_dados(url):
    if not url:
        st.error("O URL da planilha está vazio. Verifique os Secrets.")
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(url, encoding='utf-8')
        
        # Garante que colunas essenciais existam, mesmo que vazias
        colunas_essenciais = ['Report', 'Descrição', 'Link', 'Status', 'Responsável', 'Público', 'Mídia']
        for col in colunas_essenciais:
            if col not in df.columns:
                df[col] = pd.NA # Adiciona a coluna com valor Nulo se não existir
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        st.info(f"Verifique se o link da planilha está correto e se ela está publicada como CSV.")
        return pd.DataFrame()

# Carrega os dados
df = carregar_dados(URL_PLANILHA)

# --- Título Principal ---
st.title("💼 Portfólio de Dashboards de BI")
st.write("Navegue pelo nosso catálogo de dashboards. Use os filtros na barra lateral para refinar sua busca.")


# --- Lógica Principal (Filtros e Grid) ---

if not df.empty:
    # --- Barra Lateral de Filtros ---
    st.sidebar.header("Filtros do Catálogo")
    
    # Função auxiliar para criar listas de filtro (evita repetição de código)
    def criar_lista_filtro(coluna):
        # .dropna() remove valores vazios, .unique() pega só um de cada
        return ["Todos"] + sorted(list(df[coluna].dropna().unique()))

    # Filtros dinâmicos baseados nas colunas da planilha
    try:
        filtro_responsavel = st.sidebar.selectbox("Filtrar por Responsável:", criar_lista_filtro('Responsável'))
        filtro_publico = st.sidebar.selectbox("Filtrar por Público:", criar_lista_filtro('Público'))
        filtro_midia = st.sidebar.selectbox("Filtrar por Mídia:", criar_lista_filtro('Mídia'))
        filtro_status = st.sidebar.selectbox("Filtrar por Status:", criar_lista_filtro('Status'))
    except KeyError as e:
        # Erro defensivo caso uma coluna de filtro não seja encontrada
        st.sidebar.error(f"Erro: Coluna '{e.args[0]}' não encontrada na planilha. Verifique os cabeçalhos.")
        # Define padrões para o app não quebrar
        filtro_responsavel = filtro_publico = filtro_midia = filtro_status = "Todos"
    
    # --- Lógica de Filtragem ---
    df_filtrado = df

    # Aplica os filtros selecionados (se não for "Todos")
    if filtro_responsavel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Responsável'] == filtro_responsavel]
    
    if filtro_publico != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Público'] == filtro_publico]
    
    if filtro_midia != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Mídia'] == filtro_midia]

    if filtro_status != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    
    # --- Lógica de Exibição em Grid (Portfólio) ---
    
    st.write(f"### Exibindo {len(df_filtrado)} dashboards:")
    st.divider()

    # Define o número de colunas para o grid
    NUM_COLUNAS = 3 
    
    # Converte o dataframe filtrado em uma lista de dicionários
    reports_list = df_filtrado.to_dict('records')

    if not reports_list:
        st.info("Nenhum dashboard encontrado com os filtros selecionados.")

    # Itera pela lista de reports em "fatias" do tamanho do NUM_COLUNAS
    for i in range(0, len(reports_list), NUM_COLUNAS):
        
        # Cria as colunas para esta linha do grid
        cols = st.columns(NUM_COLUNAS)
        
        # Pega a "fatia" de reports para esta linha
        chunk = reports_list[i : i + NUM_COLUNAS]

        # Itera sobre a fatia e preenche cada coluna
        for j, report_data in enumerate(chunk):
            
            # 'cols[j]' é a coluna atual (coluna 0, 1 ou 2)
            with cols[j]:
                
                # 'border=True' é o que nosso CSS usa como "gatilho"
                with st.container(border=True):
                    
                    # Título do Card
                    st.subheader(report_data.get('Report', 'Sem Título'))
                    
                    # Descrição (limitada a 150 caracteres para não quebrar o layout)
                    descricao = report_data.get('Descrição', 'Sem descrição.')
                    if pd.isna(descricao): descricao = "Sem descrição."
                    st.write(descricao[:150] + ("..." if len(descricao) > 150 else ""))

                    # Informações secundárias (Público, Responsável)
                    st.caption(f"Público: {report_data.get('Público', 'N/A')} | Responsável: {report_data.get('Responsável', 'N/A')}")
                    
                    # Popover: um "botão" que abre uma janela com detalhes
                    with st.popover("Ver mais detalhes", key=f"popover_{i}_{j}"):
                        st.markdown(f"**Periodicidade:** {report_data.get('Periodicidade', 'N/A')}")
                        st.markdown(f"**Mídia:** {report_data.get('Mídia', 'N/A')}")
                        st.markdown(f"**Horário:** {report_data.get('Horário', 'N/A')}")
                        st.markdown(f"**Divulgação:** {report_data.get('Divulgação', 'N/A')}")
                        st.markdown(f"**Status:** {report_data.get('Status', 'N/A')}")
                    
                    # Botão de Ação (só aparece se o link existir)
                    link = report_data.get('Link')
                    if link and pd.notna(link):
                        st.link_button(
                            "Acessar Dashboard", 
                            link, 
                            use_container_width=True, 
                            type="primary",
                            key=f"link_{i}_{j}" # Chave única
                        )
                    else:
                        # CORREÇÃO DO ERRO: 'key' garante que cada botão desabilitado seja único
                        st.button(
                            "Link Indisponível", 
                            use_container_width=True, 
                            disabled=True, 
                            key=f"disabled_{i}_{j}" # Chave única
                        )

else:
    # Mensagem caso a planilha esteja vazia ou o carregamento falhe
    st.warning("Não foi possível carregar os dados do catálogo. Verifique a planilha ou a configuração do 'Secrets'.")

st.sidebar.info("Este catálogo é atualizado automaticamente a cada 10 minutos.")