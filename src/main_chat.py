import streamlit as st
from src.api import get_ai_response_stream
from src.chat_utils import create_new_chat
from typing import List, Dict, Any, Optional
from style.load_css import load_css
from src.activity_log import log_ai_activity

load_css()
# --- INIT ---
def initialize_session_state():
    defaults = {"is_generating": False, "stop_generation": False, "feedback_log": {}}
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


# --- FEEDBACK ---
def save_feedback(index: int):
    fb = st.session_state.get(f"feedback_{index}")
    if fb is not None:
        st.session_state.feedback_log[index] = fb
        st.toast("❤️ Cảm ơn phản hồi!" if fb == "positive" else "💬 Sẽ được cải thiện.")


# --- DISPLAY HISTORY ---
def display_chat_messages(messages: List[Dict[str, Any]]):
    for i, msg in enumerate(messages):
        if msg["role"] == "assistant" and not msg["content"].strip() and st.session_state.is_generating:
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg["content"].strip():
                fb_value = st.session_state.feedback_log.get(i)
                st.session_state[f"feedback_{i}"] = fb_value
                st.feedback(
                    "thumbs", key=f"feedback_{i}", disabled=fb_value is not None,
                    on_change=save_feedback, args=(i,)
                )


# --- CONTROLS ---
def display_chat_controls() -> tuple[Optional[str], str]:
    try:
        model_options = get_ai_response_stream()
    except Exception:
        model_options = ["default-model"]
    selected_model = st.selectbox("🧠 Model:", model_options, disabled=st.session_state.is_generating)
    col1, col2 = st.columns([10, 1])
    with col1:
        prompt = st.chat_input("Nhập câu hỏi...", disabled=st.session_state.is_generating)
    with col2:
        if st.session_state.is_generating and st.button("⏹", use_container_width=True, type="primary"):
            st.session_state.stop_generation = True
            st.toast("🛑 Dừng phản hồi")
            st.rerun()
    return prompt, selected_model


# --- HANDLE PROMPT ---
def handle_prompt_submission(prompt: str, current_chat: Dict[str, Any]):
    current_chat["messages"].append({"role": "user", "content": prompt})
    current_chat["messages"].append({"role": "assistant", "content": ""})
    st.session_state.is_generating = True


# --- STREAM RESPONSE (USING WRITE_STREAM) ---
def stream_and_display_response(current_chat: Dict[str, Any], selected_model: str):
    user_prompt = current_chat["messages"][-2]["content"]

    # log start
    log_ai_activity("🔁 Bắt đầu phản hồi", f"Prompt: {user_prompt[:60]}")

    def ai_generator():
        prev_node = None
        try:
            for packet in get_ai_response_stream(user_prompt, selected_model, activity="chat"):
                if st.session_state.stop_generation:
                    st.toast("Đã dừng")
                    break

                meta = packet.get("metadata", {})
                node = meta.get("langgraph_node", "")
                model_name = packet.get("ls_model_name", "")

                # log node change
                if node and node != prev_node:
                    log_ai_activity(f"📍 Node: {node}", f"model={model_name}", metadata=meta)
                    prev_node = node

                # yield chunk text
                yield packet.get("content_chunk", "")

        except Exception as e:
            log_ai_activity("❌ Lỗi stream", str(e))
            yield f"\n⚠️ Lỗi: {e}"
        finally:
            log_ai_activity("✅ Kết thúc phản hồi", f"Model={selected_model}")

    with st.chat_message("assistant"):
        full_text = st.write_stream(ai_generator())  # 💡 core upgrade
        st.feedback(
            "thumbs", key=f"feedback_{len(current_chat['messages'])}",
            on_change=save_feedback, args=(len(current_chat["messages"]),),
        )
    current_chat["messages"][-1]["content"] = full_text
    st.session_state.is_generating = False
    st.session_state.stop_generation = False


# --- MAIN ---
def render_chat_area():
    st.header("💬 Chat")
    initialize_session_state()

    if not st.session_state.get("current_chat_id") and not st.session_state.get("chat_history"):
        create_new_chat()
    if not st.session_state.get("current_chat_id"):
        st.info("Hãy bắt đầu chat mới từ sidebar.")
        return

    current_chat = st.session_state.chat_history[st.session_state.current_chat_id]
    chat_container = st.container(height=400)
    with chat_container:
        display_chat_messages(current_chat["messages"])

    prompt, selected_model = display_chat_controls()
    if prompt:
        handle_prompt_submission(prompt, current_chat)
        st.rerun()

    if st.session_state.is_generating and not st.session_state.stop_generation:
        with chat_container:
            stream_and_display_response(current_chat, selected_model)
        st.rerun()
