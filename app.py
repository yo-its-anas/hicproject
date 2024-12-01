import streamlit as st
import json
import requests
import time
import random
from geopy.distance import geodesic

# Load the Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")

# Blood bank dummy data
blood_banks = [
    {"name": "Indus Hospital", "location": "Korangi", "groups": ["A+", "B+", "O-", "AB+"], "contact": "021-111-111-880", "website": "https://indushospital.org"},
    {"name": "Fatimid Foundation", "location": "Clifton", "groups": ["A-", "B-", "O+", "AB-"], "contact": "021-3586-9669", "website": "https://fatimid.org"},
    {"name": "Agha Khan Blood Bank", "location": "Gulshan", "groups": ["A+", "O-", "B+"], "contact": "021-3493-0051", "website": "https://hospitals.aku.edu"},
    # Add more dummy data here
    {"name": "Hilal-e-Ahmer", "location": "Tariq Road", "groups": ["O+", "A-", "B-", "AB+"], "contact": "021-3454-3508", "website": "https://hilal.com"},
    {"name": "Saylani Blood Bank", "location": "Bahadurabad", "groups": ["A+", "O-", "B+"], "contact": "021-111-729-526", "website": "https://saylaniwelfare.com"},
    {"name": "JPMC Blood Bank", "location": "Saddar", "groups": ["A+", "O+", "AB-"], "contact": "021-3271-2097", "website": "https://jpmc.edu.pk"},
    {"name": "Ziauddin Hospital Blood Bank", "location": "North Nazimabad", "groups": ["B+", "O+", "A+"], "contact": "021-3664-4271", "website": "https://ziauddinhospital.com"},
    {"name": "OMI Hospital", "location": "Cantt", "groups": ["A-", "B-", "O-", "AB+"], "contact": "021-3225-2417", "website": "https://omihospital.com"},
    {"name": "South City Hospital", "location": "Defence", "groups": ["A+", "B+", "O+"], "contact": "021-3586-1084", "website": "https://southcityhospital.org"},
    {"name": "Karwan-e-Hayat", "location": "Keamari", "groups": ["O-", "A-", "B+"], "contact": "021-3285-9901", "website": "https://karwan-e-hayat.com"},
    {"name": "Patel Hospital", "location": "Gulistan-e-Johar", "groups": ["A+", "O-", "AB+"], "contact": "021-111-174-174", "website": "https://patel-hospital.com"},
]

# Session state for login
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

# Login function
def login(username, password):
    if username and password:  # Dummy login logic
        st.session_state['is_logged_in'] = True
        st.session_state['username'] = username
        st.experimental_rerun()

# Logout function
def logout():
    st.session_state['is_logged_in'] = False
    st.experimental_rerun()

# Display login or main app
st.set_page_config(page_title="Karachi Blood Bank Finder", page_icon="🩸", layout="wide")
if not st.session_state['is_logged_in']:
    st.title("Karachi Blood Bank Finder 🩸")
    with st.container():
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.button("Login", on_click=login, args=(username, password))
else:
    st.success(f"Welcome, {st.session_state['username']}!")
    st.button("Logout", on_click=logout)

    st.markdown("<h1 style='text-align: center; color: red;'>Karachi Blood Bank Finder 🩸</h1>", unsafe_allow_html=True)
    st_lottie = st.json(lottie_animation)

    st.write("### Select your location and blood group to find the nearest blood bank.")
    areas = ["Korangi", "Clifton", "Gulshan", "Tariq Road", "Bahadurabad", "Saddar", "North Nazimabad", "Defence", "Keamari", "Gulistan-e-Johar"]
    area = st.selectbox("Select Your Area:", areas)
    blood_group = st.selectbox("Select Required Blood Group:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

    if st.button("Find Blood Banks"):
        with st.spinner("Searching for blood banks..."):
            time.sleep(3)  # Simulate search time

        st.write("### Nearby Blood Banks")
        for bank in blood_banks:
            if bank["location"] == area and blood_group in bank["groups"]:
                st.markdown(f"""
                <div style='border: 1px solid blue; padding: 15px; margin: 10px 0;'>
                    <strong>Name:</strong> {bank['name']}<br>
                    <strong>Location:</strong> {bank['location']}<br>
                    <strong>Available Blood Groups:</strong> {", ".join(bank['groups'])}<br>
                    <strong>Contact:</strong> {bank['contact']}<br>
                    <strong>Website:</strong> <a href='{bank['website']}' target='_blank'>{bank['website']}</a>
                </div>
                """, unsafe_allow_html=True)
