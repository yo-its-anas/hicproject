import streamlit as st
from user_data import register_user

def registration_page():
    st.title("Register for Karachi Blood Bank Finder 🩸")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    contact = st.text_input("Contact Number")
    location = st.selectbox("Location", ["Korangi", "Clifton", "Gulshan", "Tariq Road", "Bahadurabad", "Saddar", "North Nazimabad", "Defence", "Keamari", "Gulistan-e-Johar"])

    if st.button("Register"):
        success, message = register_user(username, password, email, blood_group, contact, location)
        if success:
            st.success(message)
        else:
            st.error(message)
