import streamlit as st
from user_data import validate_user
from registration import registration_page

# Session state initialization
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

def login_page():
    st.title("Login to Karachi Blood Bank Finder 🩸")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        valid, user_info = validate_user(username, password)
        if valid:
            st.session_state['is_logged_in'] = True
            st.session_state['user_info'] = user_info
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

def main_page():
    st.success(f"Welcome, {st.session_state['user_info']['email']}!")
    st.write("### Main Application Page")
    st.write(f"**Blood Group:** {st.session_state['user_info']['blood_group']}")
    st.write(f"**Location:** {st.session_state['user_info']['location']}")
    st.button("Logout", on_click=lambda: logout())

def logout():
    st.session_state.clear()
    st.experimental_rerun()

st.sidebar.title("Navigation")
options = st.sidebar.radio("Choose an option", ["Login", "Register"])

if st.session_state['is_logged_in']:
    main_page()
elif options == "Register":
    registration_page()
else:
    login_page()
