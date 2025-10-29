import streamlit as st

def create_portfolio_cards(df):
    html = "<div class='portfolio-grid'>"
    for _, row in df.iterrows():
        title = row.get("Título", "Sem título")
        category = row.get("Categoria", "")
        desc = row.get("Descrição", "")
        link = row.get("Link", "#")
        image = row.get("Imagem_Path", "")

        html += f"""
        <div class="card fadeIn">
            <div class="card-image">
                {'<img src="' + image + '" alt="' + title + '">' if image else '<div class="placeholder">Sem imagem</div>'}
            </div>
            <div class="card-content">
                <h3>{title}</h3>
                <p class="category">{category}</p>
                <p class="desc">{desc}</p>
                <a href="{link}" target="_blank" class="btn">Ver Projeto</a>
            </div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
