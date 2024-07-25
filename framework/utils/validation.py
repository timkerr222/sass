import re
import streamlit as st
from email_validator import validate_email, EmailNotValidError
import bcrypt

def validate_username(username):
    if not re.match(r'^[A-Za-z0-9]{6,15}$', username):
        return False, "Username must be 6-15 characters long and contain only letters and numbers."
    return True, ""

def validate_email_address(email):
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_number(phone):
    if not re.match(r'^\+?[0-9]{10,15}$', phone):
        return False, "Phone number must be 10-15 digits long and may start with a '+' for international numbers."
    return True, ""

def validate_password(password, username, password_history, skip_history_check=False):
    results = []
    if len(password) >= 8:
        results.append((True, "At least 8 characters"))
    else:
        results.append((False, "At least 8 characters"))
    
    if re.search(r'[a-z]', password):
        results.append((True, "A lowercase letter"))
    else:
        results.append((False, "A lowercase letter"))
    
    if re.search(r'[A-Z]', password):
        results.append((True, "An uppercase letter"))
    else:
        results.append((False, "An uppercase letter"))
    
    if re.search(r'[0-9]', password):
        results.append((True, "A number"))
    else:
        results.append((False, "A number"))
    
    if re.search(r'[\W_]', password):
        results.append((True, "A symbol"))
    else:
        results.append((False, "A symbol"))
    
    if username.lower() not in password.lower():
        results.append((True, "No parts of your username"))
    else:
        results.append((False, "No parts of your username"))
    
    if not skip_history_check:
        if not any(bcrypt.checkpw(password.encode(), old_pw.encode()) for old_pw in password_history):
            results.append((True, "Your password cannot be any of your last 4 passwords"))
        else:
            results.append((False, "Your password cannot be any of your last 4 passwords"))
    
    return results

def display_password_requirements(results=None):
    st.subheader("Password requirements:")
    requirements = [
        "At least 8 characters",
        "A lowercase letter",
        "An uppercase letter",
        "A number",
        "A symbol",
        "No parts of your username",
        "Your password cannot be any of your last 4 passwords",
        "At least 1 day must have elapsed since you last changed your password"
    ]
    
    if results:
        for requirement, msg in zip(requirements, results):
            if msg[0]:
                st.markdown(f"- ✅ {requirement}")
            else:
                st.markdown(f"- ❌ {requirement}")
    else:
        for requirement in requirements:
            st.markdown(f"- {requirement}")
