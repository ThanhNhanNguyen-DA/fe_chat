import streamlit as st
from src.session_state import init_session_state
from src.sidebar import render_sidebar
from src.main_chat import render_chat_area
from src.activity_log import render_activity_log
from style.load_css import load_css
from src.login import login
from src.config import get_page_config

# ---------------- AUTH GATE ----------------
try:
    if not st.session_state.get("user_authenticated", False):
        login()
        st.stop()
except Exception:
    pass


# ========== PAGE CONFIG ==========
st.set_page_config(**get_page_config())

# ========== CSS ==========
load_css()

# ========== SESSION INIT ==========
init_session_state()

# ========== SIDEBAR ==========
render_sidebar()

# ========== MAIN LAYOUT ==========
col_chat, col_activity = st.columns([2, 1])

with col_chat:
    render_chat_area()

with col_activity:
    render_activity_log()
