import yaml
import streamlit as st
import os
import logging
from framework.utils.cookie_handler import CookieHandler


def load_routes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the config.yaml file
    config_path = os.path.join(base_dir, '../configs/routes.yaml')

    # Load the configuration from the YAML file
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)['routes']

def check_authentication():
    cookie_handler = CookieHandler(
        cookie_name=st.secrets["cookie_configs"]["cookie_name"],
        secret_key=st.secrets["cookie_configs"]["secret_key"],
        expiry_days=st.secrets["cookie_configs"]["expiry_days"],
        key=st.secrets["cookie_configs"]["key"]
    )
    authenticated_user = cookie_handler.get_cookie()
    if not authenticated_user:
        st.warning("You are not logged in. Redirecting to login page...")
        # st.stop() # Optionally stop execution if not authenticated
    return authenticated_user

def get_accessible_routes(user):
    routes = load_routes()
    accessible_routes = []
    for route in routes:
        auth_required = route.get('auth_required', False)
        roles = route.get('roles', [])
        show_nav_when_authenticated = route.get('show_nav_when_authenticated', True)
        nav_icon = route.get('nav_icon', '')

        if not auth_required or (user and (not roles or user.get('role') in roles)):
            if user and not show_nav_when_authenticated:
                continue

            display_name = f"{nav_icon} {route['name']}" if nav_icon else route['name']
            accessible_routes.append({"name": display_name, "path": route['path']})
    
    return accessible_routes

def handle_routing():
    user = check_authentication()
    accessible_routes = get_accessible_routes(user)

    page = st.sidebar.radio("Hello", options=[route['name'] for route in accessible_routes], key="user_profile_options")
    if user:
        st.sidebar.write(user)

    if page:
        route_info = next(r for r in accessible_routes if r['name'] == page)
        module = __import__( f"framework.{route_info['path']}", fromlist=[''])
        module.main(user)
      