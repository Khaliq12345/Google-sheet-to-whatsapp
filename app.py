import streamlit as st
from WhatsAppScript import *
from st_login_form import login_form

if 'to_login' not in st.session_state:
    st.session_state['to_login'] = False
    
def verify_login(username: str, password):
    match [username, password]:
        case [st.secrets.username, st.secrets.password]:
            st.session_state['to_login'] = True
            st.balloons()
            st.rerun()
        case _:
            return st.error("Username or password incorrect")

def main():
    st.set_page_config(page_title="Google Sheet to Whatsapp")
    with st.form("Send data to Whatsapp"):
        google_sheet_link = st.text_input("Your google sheet Link")
        if st.form_submit_button("Send"):
            with st.spinner():
                script.main(google_sheet_link)
            st.success("DONE!")

if st.session_state['to_login']:
    main()
else:
    with st.form("Login"):
        username = st.text_input("Username")
        password = st.text_input("Password")
        st.form_submit_button("Login", on_click=verify_login, args=(username, password))