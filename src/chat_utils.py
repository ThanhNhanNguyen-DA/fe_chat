import streamlit as st
from datetime import datetime


def log_ai_activity(action: str, details: str = "", metadata=None):
    """Ghi lại log hoạt động AI."""
    st.session_state.setdefault("activities", [])
    st.session_state.activities.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": action,
        "details": details,
        "metadata": metadata or {}
    })
    st.session_state.activities = st.session_state.activities[:15]


def create_new_chat():
    """Create a new chat with a short title."""
    chat_id = f"chat_{st.session_state.chat_counter}"
    st.session_state.chat_counter += 1
    title = f"Chat {st.session_state.chat_counter}"
    st.session_state.chat_history[chat_id] = {
        "title": title,
        "messages": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    st.session_state.current_chat_id = chat_id

    # Reset các trạng thái UI khác
    st.session_state.rename_mode = None
    st.session_state.share_chat_id = None

    return chat_id


def rename_chat(chat_id, new_name):
    """Renames a specific chat."""
    if chat_id in st.session_state.chat_history:
        st.session_state.chat_history[chat_id]["title"] = new_name.strip()[:30]


def share_chat(chat_id):
    """Show a modal with shareable chat content."""
    if chat_id in st.session_state.chat_history:
        chat_data = st.session_state.chat_history[chat_id]
        shareable_text = f"📜 {chat_data['title']}\nCreated: {chat_data['created_at']}\n\n"

        for msg in chat_data["messages"]:
            role_name = "You" if msg["role"] == "user" else "Assistant"
            shareable_text += f"{role_name}: {msg['content']}\n\n"

        # Dùng expander để hiển thị
        with st.expander("📤 Shareable Chat Preview", expanded=True):
            st.text_area(
                "Copy nội dung bên dưới:",
                value=shareable_text.strip(),
                height=200
            )
            st.download_button(
                label="📥 Tải về (.txt)",
                data=shareable_text.strip(),
                file_name=f"{chat_data['title'].replace(' ', '_')}.txt",
                mime="text/plain"
            )


def delete_chat(chat_id):
    """Deletes a specific chat."""
    if chat_id in st.session_state.chat_history:
        del st.session_state.chat_history[chat_id]

        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None

        # Reset các trạng thái UI
        st.session_state.rename_mode = None
        st.session_state.share_chat_id = None


def generate_chat_title(user_message: str):
    """Tạo tiêu đề ngắn gọn cho cuộc trò chuyện dựa vào câu hỏi đầu tiên."""
    title = user_message.strip()
    if len(title) > 30:
        title = title[:27] + "..."
    if st.session_state.current_chat_id in st.session_state.chat_history:
        st.session_state.chat_history[st.session_state.current_chat_id]["title"] = title
