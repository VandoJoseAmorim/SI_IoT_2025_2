# MEU PRIMEIRO WEB APP
import streamlit as st

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
	st.title("Meu primeiro WebApp Python")
    
if __name__ == '__main__':
	main()
    