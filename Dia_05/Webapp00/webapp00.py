# MEU PRIMEIRO WEB APP
import streamlit as st
from PIL import Image

def main():

    st.set_page_config(
        page_title="Streamlit WebApp",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://30days-tmp.streamlit.app/?ref=blog.streamlit.io',
            'Report a bug': "mailto:prof.massaki@gmail.com",
            'About': "# WebApp teste"
        }
    )

    # Exibe a figura
    image = Image.open('W:/webapp00/desenvolvimento.jpg')
    st.image(image, caption='Rótulo da Figura.')

    # Conteúdo principal
    st.header("Web Page Teste")
    st.sidebar.title('Menu')

    paginaSelecionada = st.sidebar.selectbox('Selecione a Página', ['Página 01', 'Página 02'])

    if paginaSelecionada == 'Página 01':
        st.title('Título da Página 1')
        st.selectbox('Selecione uma opção: ', ['Opção 1', 'Opção 2'])

        # Entradas de valores
        v1 = st.text_input("Digite o valor v1:")
        v2 = st.text_input("Digite o valor v2:")

        # Botão para calcular a média
        if st.button("Calcular Média"):
            try:
                v1 = float(v1)
                v2 = float(v2)
                media = (v1 + v2) / 2
                st.success(f"A média entre {v1} e {v2} é **{media:.2f}**")
            except ValueError:
                st.error("Por favor, insira valores numéricos válidos!")

    elif paginaSelecionada == 'Página 02':
        st.title('Título da Página 2')
        st.write('Desenvolvimento de minha 1ª Web Page Python - By Massaki Igarashi')
        st.title("Meu primeiro WebApp Python")

if __name__ == '__main__':
    main()
