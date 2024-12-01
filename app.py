import streamlit as st
import time
import requests
from geopy.distance import geodesic
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

lottie_animation = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")

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

blood_banks = [
    {"name": "Karachi Blood Center", "location": "Clifton", "groups": ["A+", "O+", "B-"], "contact": "021-1234567", "website": "https://karachibloodcenter.org"},
    {"name": "Fatimid Foundation", "location": "Saddar", "groups": ["AB+", "O-", "A-"], "contact": "021-7654321", "website": "https://fatimid.org"},
    {"name": "Indus Hospital", "location": "Korangi", "groups": ["B+", "O+", "A+"], "contact": "021-9988776", "website": "https://indushospital.org"},
    {"name": "Agha Khan Blood Center", "location": "Defence", "groups": ["O-", "A+", "B-"], "contact": "021-2345678", "website": "https://aku.edu"},
    {"name": "LifeLine Blood Center", "location": "Nazimabad", "groups": ["AB-", "O-", "B+"], "contact": "021-8765432", "website": "https://lifeline.pk"},
    {
        "name": "Saylani Blood Donation Center",
        "location": "Gulistan-e-Johar",
        "groups": ["A-", "O+", "AB-"],
        "contact": "021-3344556",
        "website": "https://saylaniwelfare.com"
    },
    {
        "name": "Edhi Blood Bank",
        "location": "Landhi",
        "groups": ["B-", "AB+", "O-"],
        "contact": "021-5566778",
        "website": "https://edhi.org"
    },
    {
        "name": "Pakistan Red Crescent Blood Bank",
        "location": "Saddar",
        "groups": ["A+", "AB-", "B+"],
        "contact": "021-9876543",
        "website": "https://prcs.org.pk"
    },
    {
        "name": "Jinnah Hospital Blood Center",
        "location": "Gulshan-e-Iqbal",
        "groups": ["O+", "A-", "B-"],
        "contact": "021-5678910",
        "website": "https://jinnahhospital.org"
    },
    {
        "name": "Omar Hospital Blood Bank",
        "location": "PECHS",
        "groups": ["A+", "B-", "O+"],
        "contact": "021-6677889",
        "website": "https://omarhospital.pk"
    },
    {
        "name": "Hilal-e-Ahmer Blood Center",
        "location": "Korangi",
        "groups": ["O-", "A+", "AB+"],
        "contact": "021-4455667",
        "website": "https://hilaaleahmer.org"
    },
    {
        "name": "Shifa Blood Center",
        "location": "Shah Faisal",
        "groups": ["B+", "O-", "A+"],
        "contact": "021-9988775",
        "website": "https://shifabloodcenter.pk"
    },
    {
        "name": "LifeBlood Foundation",
        "location": "Orangi Town",
        "groups": ["O+", "B-", "A-"],
        "contact": "021-1122334",
        "website": "https://lifeblood.pk"
    },
    {
        "name": "Razia Medical Blood Bank",
        "location": "Malir",
        "groups": ["AB-", "O+", "B+"],
        "contact": "021-2211445",
        "website": "https://raziamedical.pk"
    },
]

st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

if lottie_animation:
    st_lottie(lottie_animation, height=300)
else:
    st.warning("Animation unavailable. Proceeding with app.")

menu = st.radio("Navigation", ["Home", "Login", "Create Account"], horizontal=True)
logged_in = st.session_state.get("logged_in", False)

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

if menu == "Home" or logged_in:
    if not logged_in:
        blood_bank_finder()
elif menu == "Login":
    if not logged_in:
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
    else:
        blood_bank_finder(st.session_state.username)
elif menu == "Create Account":
    st.subheader("Create a New Account")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_user and new_password:
            st.success(f"Account created for {new_user}. You can now log in.")
        else:
            st.error("Please fill in both fields.")
