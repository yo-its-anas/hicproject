import json
import os

USERS_FILE = "users.json"

def load_users():
    """Loads user data from JSON file."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            json.dump({}, file)
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    """Saves user data to JSON file."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def register_user(username, password, email, blood_group, contact, location):
    """Registers a new user."""
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "password": password,
        "email": email,
        "blood_group": blood_group,
        "contact": contact,
        "location": location
    }
    save_users(users)
    return True, "Registration successful."

def validate_user(username, password):
    """Validates user login."""
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True, users[username]
    return False, None
