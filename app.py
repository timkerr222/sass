import streamlit as st
import logging
from framework.utils.route_loader import handle_routing
from framework.utils.styles import load_layout, load_style, load_logo

# Set the application screen layout properties first.
load_layout()

# Set up logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Apply CSS styles
load_logo()
load_style()

# Handle routing
handle_routing()
