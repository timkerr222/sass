import streamlit as st
import yaml
import bcrypt
import random
import os
import string
from yaml.loader import SafeLoader
from datetime import datetime, timedelta

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
    # Set page configuration
    #st.set_page_config(page_title="Admin Page", layout="wide")
  
    # Initialize configuration
    config = load_config()

    # Set page configuration

    st.title("Admin Page")

    # Inject custom CSS
    st.markdown("""
        <style>
        [data-testid='stHorizontalBlock'] {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        </style>
        """, unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs(["Active Users", "Unconfirmed Users", "Deleted Users"])

    with tabs[0]:
        st.header("Active Users")

        # Create table header
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown("**Username**")
        with col2:
            st.markdown("**Email**")
        with col3:
            st.markdown("**Name**")
        with col4:
            st.markdown("**Phone**")
        with col5:
            st.markdown("**Actions**")

        # Display active users
        for username, user_info in config['credentials']['usernames'].items():
            if user_info['account_confirmed'] and not user_info.get('is_deleted', False):
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    st.write(username)
                with col2:
                    st.write(user_info['email'])
                with col3:
                    st.write(user_info['name'])
                with col4:
                    st.write(user_info['phone'])
                with col5:
                    if st.button(f"Reset Account for {username}", key=f"reset_{username}"):
                        confirmation_code = generate_confirmation_code()
                        hashed_confirmation_code = bcrypt.hashpw(confirmation_code.encode(), bcrypt.gensalt()).decode()
                        confirmation_expiry = datetime.utcnow() + timedelta(hours=1)

                        user_info['confirmation_code'] = hashed_confirmation_code
                        user_info['confirmation_expiry'] = confirmation_expiry.isoformat()
                        user_info['failed_confirmation_attempts'] = 0
                        user_info['secret'] = None  # Remove 2FA secret
                        user_info['account_confirmed'] = False  # Mark account as unconfirmed
                        user_info['account_2fa_confirmed'] = False  # Mark account as unconfirmed

                        save_config(config)

                        st.success(f"Account for {username} has been reset. New confirmation code: {confirmation_code}")
                    
                    if st.button(f"Delete Account for {username}", key=f"delete_{username}"):
                        user_info['is_deleted'] = True  # Soft delete the account
                        save_config(config)
                        st.success(f"Account for {username} has been deleted.")

    with tabs[1]:
        st.header("Unconfirmed Users")

        # Create table header
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown("**Username**")
        with col2:
            st.markdown("**Email**")
        with col3:
            st.markdown("**Name**")
        with col4:
            st.markdown("**Phone**")
        with col5:
            st.markdown("**Actions**")

        # Display unconfirmed users
        for username, user_info in config['credentials']['usernames'].items():
            if not user_info['account_confirmed'] and not user_info.get('is_deleted', False):
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    st.write(username)
                with col2:
                    st.write(user_info['email'])
                with col3:
                    st.write(user_info['name'])
                with col4:
                    st.write(user_info['phone'])
                with col5:
                    if st.button(f"Generate Code for {username}", key=f"gen_{username}"):
                        confirmation_code = generate_confirmation_code()
                        hashed_confirmation_code = bcrypt.hashpw(confirmation_code.encode(), bcrypt.gensalt()).decode()
                        confirmation_expiry = datetime.utcnow() + timedelta(hours=1)

                        user_info['confirmation_code'] = hashed_confirmation_code
                        user_info['confirmation_expiry'] = confirmation_expiry.isoformat()
                        user_info['failed_confirmation_attempts'] = 0

                        save_config(config)

                        st.success(f"New confirmation code generated for {username}: {confirmation_code}")
                    
                    if st.button(f"Delete Account for {username}", key=f"delete_{username}"):
                        user_info['is_deleted'] = True  # Soft delete the account
                        save_config(config)
                        st.success(f"Account for {username} has been deleted.")

    with tabs[2]:
        st.header("Deleted Users")

        # Create table header
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown("**Username**")
        with col2:
            st.markdown("**Email**")
        with col3:
            st.markdown("**Name**")
        with col4:
            st.markdown("**Phone**")
        with col5:
            st.markdown("**Actions**")

        # Display deleted users
        for username, user_info in config['credentials']['usernames'].items():
            if user_info.get('is_deleted', False):
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                
                with col1:
                    st.write(username)
                with col2:
                    st.write(user_info['email'])
                with col3:
                    st.write(user_info['name'])
                with col4:
                    st.write(user_info['phone'])
                with col5:
                    if st.button(f"Restore Account for {username}", key=f"restore_{username}"):
                        user_info['is_deleted'] = False  # Restore the account
                        save_config(config)
                        st.success(f"Account for {username} has been restored.")
