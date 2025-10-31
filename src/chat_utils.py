import streamlit as st
from datetime import datetime
from typing import Dict
from src.activity_log import log_ai_activity  # ✅ import đúng

def create_new_chat():
    chat_id = f"chat_{st.session_state.chat_counter}"
    st.session_state.chat_counter += 1
    st.session_state.chat_history[chat_id] = {
        "title": f"Chat {st.session_state.chat_counter}",
        "messages": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.rename_mode = None
    st.session_state.share_chat_id = None
    return chat_id


def generate_chat_title(user_message: str):
    title = user_message.strip()
    if len(title) > 30:
        title = f"{title[:27]}..."
    if st.session_state.current_chat_id in st.session_state.chat_history:
        st.session_state.chat_history[st.session_state.current_chat_id]["title"] = title
