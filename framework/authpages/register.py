import streamlit as st
import yaml
import random
import string
import os
from yaml.loader import SafeLoader
from datetime import datetime, timedelta
import bcrypt
from framework.utils.validation import validate_username, validate_email_address, validate_phone_number

base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '../configs/config.yaml')
# Load configuration from YAML file
def load_config():
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

# Save configuration to YAML file
def save_config(config):
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Generate a random confirmation code
def generate_confirmation_code(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def main(user = None):
    # Initialize configuration
    config = load_config()


    st.title("Register New User")

    # Registration form
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_name = st.text_input("Name")
    new_phone = st.text_input("Phone Number")

    if st.button("Register User"):
        # Validate inputs
        valid_username, msg = validate_username(new_username)
        if not valid_username:
            st.error(msg)
        elif any(user['email'] == new_email for user in config['credentials']['usernames'].values()):
            st.error("Email already in use.")
        elif any(user['phone'] == new_phone for user in config['credentials']['usernames'].values()):
            st.error("Phone number already in use.")
        else:
            valid_email, msg = validate_email_address(new_email)
            if not valid_email:
                st.error(msg)
            else:
                valid_phone, msg = validate_phone_number(new_phone)
                if not valid_phone:
                    st.error(msg)
                else:
                    if new_username in config['credentials']['usernames']:
                        st.error("Username already exists.")
                    else:
                        # Generate and hash the confirmation code
                        confirmation_code = generate_confirmation_code()
                        hashed_confirmation_code = bcrypt.hashpw(confirmation_code.encode(), bcrypt.gensalt()).decode()
                        confirmation_expiry = datetime.utcnow() + timedelta(hours=1)

                        # Add new user to config
                        config['credentials']['usernames'][new_username] = {
                            'email': new_email,
                            'name': new_name,
                            'phone': new_phone,
                            'password': None,  # Password will be set during confirmation
                            'confirmation_code': hashed_confirmation_code,
                            'confirmation_expiry': confirmation_expiry.isoformat(),
                            'failed_confirmation_attempts': 0,
                            'failed_password_attempts': 0,
                            'password_history': [],
                            'account_confirmed': False,
                            'account_2fa_confirmed': False,
                            'secret': None  # Placeholder for future use
                        }

                        # Save the updated config
                        save_config(config)

                        st.success("User registered successfully!")
                        st.info(f"Your confirmation code is: {confirmation_code}")

