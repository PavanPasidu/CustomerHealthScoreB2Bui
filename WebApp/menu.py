import streamlit as st
from dashboard import dashborad
from pages.Login import Login

def authenticated_menu():
    # Show a navigation menu for authenticated users
    
    st.sidebar.page_link("pages/user.py", label="Your profile")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )

    # put the Logout button to bottom
    with st.sidebar.container(height=500,border=False):
        st.markdown("")

    def home():
        st.session_state.role =None

    st.sidebar.button('Logout',on_click=home)
    
        
    


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py",label= "Overview")

    # put the Login button to bottom
    with st.sidebar.container(height=500,border=False):
        st.markdown("")

    if not st.sidebar.button('Login'):
        dashborad()
    else:
        Login()


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()