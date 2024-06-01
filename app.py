import streamlit as st
from WhatsAppScript import *

st.set_page_config(page_title="Google Sheet to Whatsapp")

with st.form("Send data to Whatsapp"):
    google_sheet_link = st.text_input("Your google sheet Link")
    if st.form_submit_button("Send"):
        with st.spinner():
            script.main(google_sheet_link)
        st.success("DONE!")