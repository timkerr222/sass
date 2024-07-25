import streamlit as st
import extra_streamlit_components as stx
import jwt
from datetime import datetime, timedelta

class CookieHandler:
    def __init__(self, cookie_name, secret_key, expiry_days, key):
        self.cookie_name = cookie_name
        self.secret_key = secret_key
        self.expiry_days = expiry_days
        self.key = key

        # Use the same CookieManager instance across the app
        if 'cookie_manager' not in st.session_state:
            st.session_state.cookie_manager = stx.CookieManager()
        self.cookie_manager = st.session_state.cookie_manager

    def set_cookie(self, username):
        exp_time = datetime.utcnow() + timedelta(days=self.expiry_days)
        token = jwt.encode({'username': username, 'exp': exp_time}, self.secret_key, algorithm='HS256')
        self.cookie_manager.set(self.cookie_name, token, expires_at=exp_time, key=self.key)

    def get_cookie(self):
        cookies = self.cookie_manager.get_all()
        token = cookies.get(self.cookie_name)
        if token:
            try:
                decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
                if decoded['exp'] > datetime.utcnow().timestamp():
                    return decoded['username']
            except jwt.ExpiredSignatureError:
                return None
        return None


class CheckCookie:
    def __init__(self, cookie_name):
        self.cookie_name = cookie_name
    
    def cookie_exists(cookie_name):
        if "get_all" not in st.session_state:
            st.session_state.get_all = []

        if cookie_name in st.session_state.get_all:
            return True
        
        return False
