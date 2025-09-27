import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Sensores | Google Sheets",
    page_icon="📊",
    layout="wide"
)

# --- Título do Webapp ---
st.title("📈 Dashboard de Monitoramento de Sensores")
st.markdown("Este webapp exibe dados de sensores coletados em tempo real a partir de uma planilha do Google Sheets.")

# --- Carregamento de Dados com Cache ---
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS2wRT11_aFFxNrTiGECHYpVm8jGQ-0pSrkhobmGOD1TITXduEMgwnZAcqGuUZMF3xLDNZXDtJXKcXR/pub?gid=205634045&single=true&output=csv"

@st.cache_data(ttl=180 ) # Cache expira a cada 3 minutos
def carregar_dados(url):
    """
    Busca os dados da URL do Google Sheets e os carrega em um DataFrame Pandas.
    """
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados_bytes = resposta.content
        df = pd.read_csv(BytesIO(dados_bytes), index_col=0)
        
        # --- Limpeza e Preparação dos Dados ---
        df.index = pd.to_datetime(df.index)
        
        # Garante que as colunas de sensores são numéricas
        df['Temperatura'] = pd.to_numeric(df['Temperatura'], errors='coerce')
        df['Umidade'] = pd.to_numeric(df['Umidade'], errors='coerce')
        
        # *** CORREÇÃO ADICIONADA AQUI ***
        # Garante que as colunas de estado também sejam numéricas (0 ou 1)
        df['Botao'] = pd.to_numeric(df['Botao'], errors='coerce')
        df['Alarme'] = pd.to_numeric(df['Alarme'], errors='coerce')
        
        # Remove linhas onde a conversão para número falhou em colunas essenciais
        df.dropna(subset=['Temperatura', 'Umidade', 'Botao', 'Alarme'], inplace=True)
        
        return df
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar os dados: {e}")
        return pd.DataFrame()

# Carrega os dados
df = carregar_dados(URL_CSV)

# Botão para recarregar
if st.button('Recarregar Dados Agora'):
    st.cache_data.clear()
    st.rerun()

# --- Exibição dos Dados ---
if not df.empty:
    st.header("🌡️ Gráfico de Temperatura e Umidade")
    st.write("Visualização da variação dos sensores ao longo do tempo.")
    st.line_chart(df[['Temperatura', 'Umidade']])

    # --- Exibição dos Estados do Botão e Alarme ---
    st.header("🚦 Status Atuais (Última Leitura)")
    
    ultimo_status = df.iloc[-1]
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Botão")
        # *** CORREÇÃO PRINCIPAL AQUI ***
        # Compara com o valor numérico 1 em vez do texto "Ligado"
        if ultimo_status['Botao'] == 1:
            st.success("Ligado") # Verde
        else:
            st.error("Desligado") # Vermelho

    with col2:
        st.subheader("Alarme")
        # *** CORREÇÃO PRINCIPAL AQUI ***
        # Compara com o valor numérico 1 em vez do texto "Ligado"
        if ultimo_status['Alarme'] == 1:
            st.success("Ligado") # Verde
        else:
            st.error("Desligado") # Vermelho

    with st.expander("Ver Tabela de Dados Completa"):
        st.dataframe(df)
else:
    st.warning("Não foi possível carregar os dados. Verifique a URL e sua conexão com a internet.")

