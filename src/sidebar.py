import streamlit as st
from src.chat_utils import create_new_chat, rename_chat, delete_chat, share_chat, generate_chat_title

def render_sidebar():
    """Render sidebar, chat history, và các nút điều khiển (phiên bản không dùng st_click_detector)."""
    
    with st.sidebar:
        st.title("🤖 AI Chatbot")

        # --- New Chat Button ---
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.trigger_create_new_chat = True

        if st.session_state.get("trigger_create_new_chat", False):
            create_new_chat()
            st.session_state.trigger_create_new_chat = False
            st.rerun()

        # st.subheader("📜 Chat History")

        # # --- Share ---
        # if st.session_state.get("share_chat_id"):
        #     chat_id_to_share = st.session_state.share_chat_id
        #     st.session_state.share_chat_id = None
        #     share_chat(chat_id_to_share)

        # # --- Rename ---
        # if st.session_state.get("rename_mode"):
        #     chat_id_to_rename = st.session_state.rename_mode
        #     current_title = st.session_state.chat_history[chat_id_to_rename]["title"]

        #     with st.form(key="rename_form"):
        #         new_title = st.text_input("New chat title:", value=current_title)
        #         col1, col2 = st.columns(2)
        #         with col1:
        #             if st.form_submit_button("Save", use_container_width=True, type="primary"):
        #                 rename_chat(chat_id_to_rename, new_title)
        #                 st.session_state.rename_mode = None
        #                 st.rerun()
        #         with col2:
        #             if st.form_submit_button("Cancel", use_container_width=True):
        #                 st.session_state.rename_mode = None
        #                 st.rerun()

        # # --- Hiển thị lịch sử chat ---
        # if not st.session_state.get("chat_history"):
        #     st.info("No chats yet. Create one!")
        # else:
        #     sorted_chat_ids = sorted(
        #         st.session_state.chat_history.keys(), 
        #         key=lambda x: int(x.split('_')[-1]), 
        #         reverse=True
        #     )

        #     for chat_id in sorted_chat_ids:
        #         chat_data = st.session_state.chat_history[chat_id]
        #         is_active = (chat_id == st.session_state.current_chat_id)

        #         # --- Giao diện hiển thị ---
        #         cols = st.columns([5, 1])
        #         with cols[0]:
        #             btn_label = f"💬 {chat_data['title']}"
        #             if is_active:
        #                 st.button(btn_label, key=f"active_{chat_id}", use_container_width=True, disabled=True)
        #             else:
        #                 if st.button(btn_label, key=f"select_{chat_id}", use_container_width=True):
        #                     st.session_state.current_chat_id = chat_id
        #                     st.session_state.rename_mode = None
        #                     st.session_state.share_chat_id = None
        #                     st.rerun()

        #         with cols[1]:
        #             with st.popover("⋮", use_container_width=False):
        #                 if st.button("✏️ Rename", key=f"rename_{chat_id}", use_container_width=True):
        #                     st.session_state.rename_mode = chat_id
        #                     st.session_state.share_chat_id = None
        #                     st.rerun()
                            
        #                 if st.button("📤 Share", key=f"share_{chat_id}", use_container_width=True):
        #                     st.session_state.share_chat_id = chat_id
        #                     st.session_state.rename_mode = None
        #                     st.rerun()

        #                 if st.button("🗑️ Delete", key=f"delete_{chat_id}", use_container_width=True, type="secondary"):
        #                     delete_chat(chat_id)
        #                     st.rerun()
