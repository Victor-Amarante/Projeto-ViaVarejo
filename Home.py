import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import os
import base64
from io import StringIO, BytesIO
from utils import bg_page

# funcao para baixar a base de dados
def generate_excel_download_link(df, i):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="base.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

# personalizando algumas config iniciais do sistema
st.set_page_config(page_title='QCA - Via Varejo', layout='wide')

# defininco o layout da pagina
bg_page('bg_dark.png')
hide_menu = """
<style>
#MainMenu {
    visibility:visible;
}

footer {
    visibility:visible;
}

footer:before {
    content:'Desenvolvido pela Eficiência Jurídica - Controladoria Jurídica';
    display:block;
    position:relative;
    color:#6c6a76;
}
</style>
"""

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
    with st.sidebar:
        st.title(f"Bem-vindo(a), {name.split()[0] + ' ' + name.split()[1]}!")
        authenticator.logout("Logout", "sidebar")
    
    # Titulo da pagina
    st.markdown('# Programa QCA - Via Varejo')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
            ##### Com essa ferramenta, será possível fazer o tratamendo da base de dados principal de maneira simples, rápida e eficaz.
        ''')

    st.divider()
    st.write('\n')

    col3, col4 = st.columns(2)
    with col3:
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.markdown('''
            ##### Têm dúvidas sobre como utilizar a automação? Verifique o tutorial ao lado...👉
        ''')
    # with col4:
    #     video_file = open('teste.mp4', 'rb')
    #     video_bytes = video_file.read()
    #     st.video(video_bytes)
    
    st.divider()
    st.write('\n')

    with st.container():
        col5, col6 = st.columns(2)
        with col5:
            st.markdown('''
                ###### Para entrar em contato e esclarecer dúvidas, por favor, envie sua mensagem abaixo. :red[*Resposta em até 24 horas!*]
            ''')
            contact_form = """
            <form action="https://formsubmit.co/victoramarante@queirozcavalcanti.adv.br" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Digite o seu nome" required>
                <input type="email" name="email" placeholder="Digite o seu e-mail do escritório" required>
                <textarea name="message" placeholder="Escreva a sua dúvida, sugestão, feedback..."></textarea>
                <button type="submit">Enviar</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
            # Use Local CSS File
            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            local_css("style/style.css")
    
