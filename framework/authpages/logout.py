import streamlit as st
import extra_streamlit_components as stx
import uuid

def main(user = None):
    # Initialize cookie manager with a unique key
    cookie_manager = stx.CookieManager(key="kill")
    cookie_name = st.secrets["cookie_configs"]["cookie_name"]
    
    try:
        cookie_manager.delete(cookie_name)
        
        st.success("You have been logged out successfully.")
            
        # Clear the session state
        st.session_state.clear()
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    except:
         # Clear the session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.warning("No active session found.")

    # Redirect to login page
    st.link_button("Go to Login", "/")

if __name__ == "__main__":
    main()
