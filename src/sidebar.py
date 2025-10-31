import streamlit as st
from src.chat_utils import create_new_chat

def render_sidebar():
    """Sidebar đơn giản với nút New Chat."""
    with st.sidebar:
        st.title("🤖 Chatbot")

        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            create_new_chat()
            st.rerun()
