import streamlit as st
import yaml
import bcrypt
import os
import pyotp
from yaml.loader import SafeLoader
from framework.utils.validation import validate_password
from framework.utils.cookie_handler import CookieHandler

base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, '../configs/config.yaml')

# Load configuration from YAML file
def load_config():
    # Construct the path to the config.yaml file
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

# Save configuration to ensure any changes are stored
def save_config(config):
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def main(user = None):
    # Initialize configuration
    config = load_config()

    # Initialize cookie handler
    cookie_handler = CookieHandler(
        cookie_name=st.secrets["cookie_configs"]["cookie_name"], 
        secret_key=st.secrets["cookie_configs"]["secret_key"], 
        expiry_days=st.secrets["cookie_configs"]["expiry_days"], 
        key=st.secrets["cookie_configs"]["key"]
    )

    # Check if user is already authenticated
    
    if user:
        st.success(f"Welcome back, {user}!")
        st.write(f"[Proceed to Main](/main.py)")
        st.stop()

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 'login'

    if 'username' not in st.session_state:
        st.session_state.username = user or ''

    if 'password' not in st.session_state:
        st.session_state.password = ''

    if 'auth_code' not in st.session_state:
        st.session_state.auth_code = ''

    # Step 1: Prompt for username and password
    if st.session_state.step == 'login':
        st.header('Login')
        st.session_state.username = st.text_input("Username")
        st.session_state.password = st.text_input("Password", type="password")

        if st.button("Submit"):
            if st.session_state.username not in config['credentials']['usernames']:
                st.error("Username or password is incorrect.")
            else:
                user = config['credentials']['usernames'][st.session_state.username]
                password_validation_results = validate_password(st.session_state.password, st.session_state.username, user['password_history'], skip_history_check=True)
                if all(result[0] for result in password_validation_results):
                    if bcrypt.checkpw(st.session_state.password.encode(), user['password'].encode()):
                        st.session_state.step = '2fa'
                    else:
                        st.error("Username or password is incorrect.")
                else:
                    st.error("Username or password is incorrect.")

    # Step 2: Prompt for 2FA code
    if st.session_state.step == '2fa':
        st.success("Password is correct.")
        user = config['credentials']['usernames'][st.session_state.username]
        if not user.get('secret'):
            st.error("2FA is not set up for this account. Please contact support.")
        else:
            st.session_state.auth_code = st.text_input("Enter the code from your authenticator app:", key="authenticator_code")
            if st.button("Verify 2FA"):
                totp = pyotp.TOTP(user['secret'])
                if totp.verify(st.session_state.auth_code):
                    st.success(f"2FA verification successful for {st.session_state.username}!")
                    cookie_handler.set_cookie(st.session_state.username)
                    st.session_state.step = 'authenticated'
                else:
                    st.error("Invalid 2FA code. Please try again.")

    # Step 3: Authenticated
    if st.session_state.step == 'authenticated':
        st.success(f"Welcome, {st.session_state.username}!")
        st.write(f"[Proceed to Main](/main.py)")

# Run the main function
if __name__ == "__main__":
    main()
