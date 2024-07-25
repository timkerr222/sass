# custom_logger.py
import logging
import streamlit as st

def setup_logger():
    """Function to set up a logger using configurations from secrets.toml."""
    logger_name = st.secrets["logger_configs"]["name"]
    log_file = st.secrets["logger_configs"]["log_file"]
    log_level = st.secrets["logger_configs"]["level"]

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level))
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    
    return logger
