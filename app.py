import streamlit as st
import time
import requests
from geopy.distance import geodesic
from streamlit_lottie import st_lottie

# Load Lottie Animation
def load_lottieurl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Preferred Lottie Animation URL
lottie_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")

# Dummy user accounts for demonstration
user_accounts = {"admin": "password123", "user1": "pass123", "test": "test"}

# Karachi Areas with Coordinates (Dummy)
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

# Dummy Blood Banks with Expanded List
blood_banks = [
    {"name": "Karachi Blood Center", "location": "Clifton", "groups": ["A+", "O+", "B-"], "contact": "021-1234567", "website": "https://karachibloodcenter.org"},
    {"name": "Fatimid Foundation", "location": "Saddar", "groups": ["AB+", "O-", "A-"], "contact": "021-7654321", "website": "https://fatimid.org"},
    {"name": "Indus Hospital", "location": "Korangi", "groups": ["B+", "O+", "A+"], "contact": "021-9988776", "website": "https://indushospital.org"},
    {"name": "Agha Khan Blood Center", "location": "Defence", "groups": ["O-", "A+", "B-"], "contact": "021-2345678", "website": "https://aku.edu"},
    {"name": "LifeLine Blood Center", "location": "Nazimabad", "groups": ["AB-", "O-", "B+"], "contact": "021-8765432", "website": "https://lifeline.pk"},
    {"name": "Jinnah Blood Bank", "location": "Malir", "groups": ["A-", "O+", "B-"], "contact": "021-1239876", "website": "https://jinnah.pk"},
    {"name": "Al-Mustafa Welfare", "location": "PECHS", "groups": ["A+", "B+", "AB+"], "contact": "021-6789654", "website": "https://almustafawelfare.org"},
    {"name": "Owais Qarni Trust", "location": "Gulberg", "groups": ["O+", "A-", "B-"], "contact": "021-7861234", "website": "https://owaisqarni.pk"},
    {"name": "Pakistan Red Crescent", "location": "Landhi", "groups": ["AB+", "A+", "O-"], "contact": "021-4356789", "website": "https://prcs.org.pk"},
    {"name": "Al-Khidmat Foundation", "location": "North Karachi", "groups": ["B+", "O-", "AB-"], "contact": "021-1234098", "website": "https://alkhidmat.org"},
]

# Streamlit Configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

# Navigation Options
menu = ["Home", "Login", "Create Account"]
choice = st.sidebar.selectbox("Menu", menu)

# Lottie Animation
if lottie_animation:
    st_lottie(lottie_animation, height=300)
else:
    st.warning("Animation unavailable. Proceeding with app.")

# Home Page or Blood Bank Finder
def blood_bank_finder(username=None):
    st.markdown("<h1 style='text-align: center; color: red;'>Karachi Blood Bank Finder 🩸</h1>", unsafe_allow_html=True)
    if username:
        st.success(f"Welcome, {username}!")
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

# Handle Menu Choices
if choice == "Home":
    blood_bank_finder()

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in user_accounts and user_accounts[username] == password:
            st.success(f"Logged in as {username}")
            blood_bank_finder(username)
        else:
            st.error("Invalid username or password")

elif choice == "Create Account":
    st.subheader("Create a New Account")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_user and new_password:
            user_accounts[new_user] = new_password
            st.success(f"Account created for {new_user}. You can now log in.")
        else:
            st.error("Please fill in both fields.")
