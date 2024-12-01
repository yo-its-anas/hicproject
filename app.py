import streamlit as st
import time
import requests
from geopy.distance import geodesic

# Import Lottie animation support
from streamlit_lottie import st_lottie

# Load Lottie Animation
def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Lottie Animation URL
blood_animation = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_bouu4z6f.json")

# Karachi Areas with Coordinates (Dummy Coordinates)
areas_coordinates = {
    "Clifton": (24.8138, 67.0353),
    "Saddar": (24.8608, 67.0104),
    "Korangi": (24.8307, 67.1326),
    "Gulshan-e-Iqbal": (24.9301, 67.1129),
    "Defence": (24.8040, 67.0697),
    "Nazimabad": (24.9066, 67.0248),
    "North Karachi": (24.9757, 67.0568),
    "PECHS": (24.8679, 67.0504),
    "Liaquatabad": (24.8972, 67.0406),
    "Malir": (24.8928, 67.1922),
    "Orangi Town": (24.9588, 66.9748),
    "Landhi": (24.8512, 67.1998),
    "Shah Faisal": (24.8677, 67.1840),
    "Gulberg": (24.9152, 67.0802),
    "Federal B Area": (24.9344, 67.0833),
}

# Expanded Dummy Blood Bank Data
blood_banks = [
    {"name": "Karachi Blood Center", "location": "Clifton", "groups": ["A+", "O+", "B-"], "contact": "021-1234567", "website": "https://karachibloodcenter.org"},
    {"name": "Fatimid Foundation", "location": "Saddar", "groups": ["AB+", "O-", "A-"], "contact": "021-7654321", "website": "https://fatimid.org"},
    {"name": "Indus Hospital Blood Center", "location": "Korangi", "groups": ["B+", "O+", "A+"], "contact": "021-9988776", "website": "https://indushospital.org"},
    {"name": "Agha Khan Blood Center", "location": "Defence", "groups": ["O-", "A+", "B-"], "contact": "021-2345678", "website": "https://aku.edu"},
    {"name": "LifeLine Blood Center", "location": "Nazimabad", "groups": ["AB-", "O-", "B+"], "contact": "021-8765432", "website": "https://lifeline.pk"},
    {"name": "Jinnah Hospital Blood Bank", "location": "Malir", "groups": ["A-", "O+", "B-"], "contact": "021-1239876", "website": "https://jinnah.pk"},
    # Add 10+ more dummy banks as needed for college display.
]

# Streamlit Configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="centered")

# Lottie Animation at the top
st_lottie(blood_animation, height=300)

st.markdown("<h1 style='text-align: center; color: red;'>Karachi Blood Bank Finder 🩸</h1>", unsafe_allow_html=True)

# Sidebar for Login/Signup
st.sidebar.title("User Authentication")
auth_status = False

if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

user_choice = st.sidebar.radio("Choose an option:", ["Login", "Create Account"])
if user_choice == "Create Account":
    new_username = st.sidebar.text_input("Enter Username")
    new_password = st.sidebar.text_input("Enter Password", type="password")
    if st.sidebar.button("Sign Up"):
        st.sidebar.success("Account created successfully! Please log in.")
elif user_choice == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        st.session_state["user_authenticated"] = True
        st.sidebar.success(f"Welcome, {username}!")

if st.session_state["user_authenticated"]:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"user_authenticated": False}))
    
    selected_area = st.selectbox("Select Your Area:", list(areas_coordinates.keys()))
    selected_blood_group = st.selectbox("Select Required Blood Group:", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    
    if st.button("Find Blood Banks"):
        with st.spinner("Searching..."):
            time.sleep(3)
        found_banks = []
        for bank in blood_banks:
            distance = geodesic(areas_coordinates[selected_area], areas_coordinates[bank["location"]]).km
            if selected_blood_group in bank["groups"]:
                found_banks.append((bank, f"{distance:.2f} km"))
                
        if found_banks:
            st.success("Blood Banks Found:")
            for bank, distance in found_banks:
                st.markdown(f"""
                <div style='border: 2px solid blue; padding: 10px; margin: 10px 0; border-radius: 8px;'>
                <strong>{bank["name"]}</strong><br>
                📍 Location: {bank["location"]} ({distance})<br>
                💉 Available Groups: {', '.join(bank["groups"])}<br>
                📞 Contact: {bank["contact"]}<br>
                🌐 <a href='{bank["website"]}' target='_blank'>Website</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("No blood banks found for your selected criteria.")
else:
    st.info("Please log in or create an account.")
