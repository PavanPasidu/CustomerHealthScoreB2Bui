import streamlit as st
from menu import menu_with_redirect
from dashboard import dashborad
from individual_dashboard import individual_dashboard

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu_with_redirect()

# st.set_page_config(page_title='Survey Results')
# st.header('Customer Health')
individual_dashboard()




