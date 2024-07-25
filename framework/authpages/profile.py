import streamlit as st
import yaml
import bcrypt
import pyotp
from io import BytesIO
import qrcode
import os
from PIL import Image
from yaml.loader import SafeLoader
from datetime import datetime
from framework.utils.validation import validate_password, display_password_requirements

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

def main(user=None):
    # Initialize configuration
    config = load_config()

    # Set page configuration
    app_name = st.secrets["application_configs"]["name"]

    st.title("Account Profile")
   
    # Confirmation form
    if not user:

        username = st.text_input("Username")

        if username:
            if username not in config['credentials']['usernames']:
                st.error("Username does not exist.")
            else:
                checkuser = config['credentials']['usernames'][username]

                if checkuser['account_confirmed']:
                    if not checkuser.get('account_2fa_confirmed', False):
                        st.subheader("Setup Two-Factor Authentication (2FA)")
                        if not checkuser.get('secret'):
                            secret = pyotp.random_base32()
                            checkuser['secret'] = secret
                            save_config(config)
                        else:
                            secret = checkuser['secret']
                        
                        st.success("2FA Secret generated. Scan the QR code below with your authenticator app.")

                        # Generate QR code for the 2FA secret
                        totp = pyotp.TOTP(secret)
                        qr_code_url = totp.provisioning_uri(username, issuer_name=app_name)
                        qr = qrcode.make(qr_code_url)
                        buffer = BytesIO()
                        qr.save(buffer, format="PNG")
                        buffer.seek(0)
                        image = Image.open(buffer)
                        st.image(image, caption="Scan this QR code", use_column_width=False, width=300)

                        code_input = st.text_input("Enter the code from your authenticator app:", key="authenticator_code")
                        if st.button("Verify 2FA Code"):
                            if totp.verify(code_input):
                                st.success(f"2FA setup successful for {username}!")
                                checkuser['account_2fa_confirmed'] = True
                                save_config(config)
                                st.write(f"[Login here](/pages/login.py)")
                            #  st.experimental_rerun()
                            else:
                                st.error("Invalid 2FA code. Please try again.")
                    else:
                        st.success("Account confirmed and 2FA is already enabled for your account.")
                        st.write(f"**Username:** {username}")
                        st.write(f"**Email:** {checkuser['email']}")
                        st.write(f"**Name:** {checkuser['name']}")
                        st.write(f"**Phone:** {checkuser['phone']}")
                        st.write(f"[Login here](login)")
                    
                elif checkuser['failed_confirmation_attempts'] >= 3:
                    st.error("Too many failed attempts. Your account is locked.")
                    if st.button("Forgot my confirmation code"):
                        checkuser['confirmation_code'] = None
                        checkuser['confirmation_expiry'] = None
                        save_config(config)
                        st.success("Your confirmation code has been reset. Please request a new one.")
                else:
                    confirmation_code = st.text_input("Confirmation Code")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm New Password", type="password")

                    if new_password:
                        password_validation_results = validate_password(new_password, username, checkuser['password_history'])
                    else:
                        password_validation_results = []

                    if st.button("Confirm"):
                        if datetime.fromisoformat(checkuser['confirmation_expiry']) < datetime.utcnow():
                            st.error("Confirmation code has expired.")
                        elif bcrypt.checkpw(confirmation_code.encode(), checkuser['confirmation_code'].encode()):
                            valid_password = all(result[0] for result in password_validation_results)
                            if not valid_password:
                                st.error("Password does not meet all requirements.")
                            elif new_password != confirm_password:
                                st.error("Passwords do not match.")
                            else:
                                st.success("Account confirmed successfully!")
                                hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                                checkuser['password'] = hashed_password
                                checkuser['confirmation_code'] = None
                                checkuser['confirmation_expiry'] = None
                                checkuser['failed_confirmation_attempts'] = 0
                                checkuser['account_confirmed'] = True
                                checkuser['password_last_changed'] = datetime.utcnow().isoformat()
                                # Update password history
                                checkuser['password_history'].append(hashed_password)
                                if len(checkuser['password_history']) > 4:
                                    checkuser['password_history'].pop(0)
                                save_config(config)
                                st.experimental_rerun()
                        else:
                            checkuser['failed_confirmation_attempts'] += 1
                            save_config(config)
                            st.error("Invalid confirmation code.")
                        
                    if st.button("Forgot my confirmation code"):
                        checkuser['confirmation_code'] = None
                        checkuser['confirmation_expiry'] = None
                        save_config(config)
                        st.success("Your confirmation code has been reset. Please request a new one.")

        if username and username in config['credentials']['usernames']:
            checkuser = config['credentials']['usernames'][username]
            if not checkuser['account_confirmed'] and checkuser['failed_confirmation_attempts'] < 3:
                display_password_requirements(password_validation_results if new_password else None)

    else:
        # Display user details if the account is confirmed and 2FA is enabled
        checkuser = config['credentials']['usernames'][user]
        if checkuser['account_confirmed'] and checkuser.get('account_2fa_confirmed', False):
            st.success("Account confirmed and 2FA is already enabled for your account.")
            st.write(f"**Username:** {user}")
            st.write(f"**Email:** {checkuser['email']}")
            st.write(f"**Name:** {checkuser['name']}")
            st.write(f"**Phone:** {checkuser['phone']}")
            st.write(f"[Login here](login)")
        else:
            st.error("Account not confirmed or 2FA not enabled.")

