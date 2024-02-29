import streamlit as st
from menu import menu
from dashboard import dashborad
from pages.Login import Login

st.set_page_config(
    page_title = 'Dashboard',
    page_icon = '✅',
    layout = 'wide'
)


# Login()
menu()