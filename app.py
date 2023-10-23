import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# personalizando algumas config iniciais do sistema
st.set_page_config(page_title='QCA DataBoost', layout='wide')

# --- USER AUTHENTICATION ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# buscando todas as informacoes necessarias de autenticacao do usuario como o username, name e senha
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# pegando informacoes especificas de cada usuario para validacao
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:   # se o nome do usuario ou a senha estiverem incorretos, mandar mensagem de erro
    st.error('Usuário/senha incorretos')

elif authentication_status == None:   # se nao tiver o username ou a senha, mandar mensagem de alerta
    st.warning('Por favor inserir informações de usuário e senha')

elif authentication_status:   # se o username e a senha estiverem corretos, seguir para entrar no sistema
    st.title('Início do programa completo de integração das automações da Controladoria Jurídica')
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")