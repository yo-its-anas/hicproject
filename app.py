import streamlit as st
import json

# Load user data
def load_user_data():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save user data
def save_user_data(data):
    with open("users.json", "w") as f:
        json.dump(data, f)

# Handle the login process
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        st.success(f"Welcome, {st.session_state.username}!")
        main_page()
    else:
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            users = load_user_data()
            if username in users and users[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.experimental_rerun()  # Avoid looping on main page
            else:
                st.error("Invalid username or password.")

# Main Page
def main_page():
    st.subheader(f"Karachi Blood Bank Finder ❤️")
    st.write(f"Hello, **{st.session_state.username}**! Please select your area and blood group.")
    # Add area and blood group selection logic here

# Logout Functionality
def logout():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()

# Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Login", "Sign Up", "Main Page"])

if option == "Login":
    login()
elif option == "Sign Up":
    st.write("Signup logic goes here.")
elif option == "Main Page":
    if "authenticated" in st.session_state and st.session_state.authenticated:
        main_page()
        logout()
    else:
        st.warning("Please log in first.")
