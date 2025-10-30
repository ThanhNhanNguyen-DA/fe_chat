import streamlit as st
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ActivityEntry:
    time: str
    action: str
    details: str
    metadata: Optional[Dict[str, Any]] = None

    @staticmethod
    def create(action: str, details: str = "", metadata=None):
        return ActivityEntry(
            time=datetime.now().strftime("%H:%M:%S"),
            action=action,
            details=details,
            metadata=metadata or {},
        )


def log_ai_activity(action: str, details: str = "", metadata=None) -> Dict[str, Any]:
    """Ghi log và trả về dict (dùng cho stream)."""
    entry = ActivityEntry.create(action, details, metadata)
    entry_dict = asdict(entry)
    st.session_state.setdefault("activities", [])
    st.session_state.activities.append(entry_dict)
    return entry_dict


def create_new_chat():
    """Tạo chat mới."""
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
    """Sinh tiêu đề ngắn gọn từ câu đầu tiên."""
    title = user_message.strip()
    if len(title) > 30:
        title = f"{title[:27]}..."
    if st.session_state.current_chat_id in st.session_state.chat_history:
        st.session_state.chat_history[st.session_state.current_chat_id]["title"] = title
