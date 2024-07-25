import streamlit as st
import yaml
import os

def load_layout():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the config.yaml file
    config_path = os.path.join(base_dir, '../configs/config.yaml')
    
    # Load the configuration from the YAML file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Set page title and layout
    page_title = config.get('page_title', 'Default App Title')
    layout = config.get('layout', 'wide')
    sidebar = config.get('sidebar', "auto")
    
    st.set_page_config(page_title=page_title, layout=layout, initial_sidebar_state=sidebar)

def load_logo():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the config.yaml file
    config_path = os.path.join(base_dir, '../configs/config.yaml')
    
    # Load the configuration from the YAML file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    logo_config = config['application_configs'].get('logo', None)

    # Check if logo is provided and the file exists
    if logo_config:
        logo_path = os.path.join(base_dir, '../images', logo_config.get('file', ''))
        width = logo_config.get('width', None)  # Optional width parameter
        alt_text = logo_config.get('alt', 'Logo')  # Optional alt text parameter
        use_container_width = logo_config.get('use_container_width', False)  # Optional container width parameter

        if os.path.exists(logo_path):
            st.sidebar.image(logo_path, width=width, use_column_width=use_container_width)
        else:
            if alt_text != 'Logo':
                st.sidebar.write(alt_text)
            st.warning("Specified logo not found. Please check the configuration.")
    else:
        pass

def load_style():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the config.yaml file
    config_path = os.path.join(base_dir, '../configs/config.yaml')
    
    # Load the configuration from the YAML file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    styles = config['application_configs'].get('styles', [])
    hide_toolbar = config['application_configs'].get('hide_streamlit_toolbar', False)
    
    for style in styles:
        style_path = os.path.join(base_dir, '../styles', f"{style}.css")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r') as file:
                    style_css = file.read()
                    # Sanitize the CSS (though CSS can't contain JavaScript)
                    style_css = style_css.replace('<script>', '&lt;script&gt;').replace('</script>', '&lt;/script&gt;')
                    st.markdown(f"<style>{style_css}</style>", unsafe_allow_html=True)
            except FileNotFoundError:
                st.toast("Style file not found. Please check the configuration.")
        else:
            st.toast("Specified style not found. Using default style.")
    
    # Optionally hide the Streamlit toolbar
    if hide_toolbar:
        st.markdown(
            """
            <style>
                [data-testid="stToolbar"] { display: none; }
            </style>
            """,
            unsafe_allow_html=True
        )
