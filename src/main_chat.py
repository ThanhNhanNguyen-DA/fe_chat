import streamlit as st
from src.api import get_ai_response_stream
from src.chat_utils import create_new_chat
from typing import List, Dict, Any, Optional


# --- 1. Khởi tạo Session State ---
def initialize_session_state():
    defaults = {
        "is_generating": False,
        "stop_generation": False,
        "feedback_log": {},  # Lưu feedback dạng {index: "positive"/"negative"}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# --- 2. Lưu feedback ---
def save_feedback(index: int):
    """Hàm callback khi người dùng bấm feedback."""
    fb = st.session_state.get(f"feedback_{index}")
    if fb is not None:
        st.session_state.feedback_log[index] = fb
        st.toast(
            "❤️ Cảm ơn bạn đã góp ý!" if fb == "positive"
            else "💬 Cảm ơn phản hồi, chúng tôi sẽ cải thiện."
        )


# --- 3. Hiển thị tin nhắn & feedback ---
def display_chat_messages(messages: List[Dict[str, Any]]):
    """Hiển thị toàn bộ lịch sử chat cùng feedback đẹp."""
    for i, msg in enumerate(messages):
        # Bỏ qua assistant đang stream (rỗng)
        if msg["role"] == "assistant" and msg.get("content", "").strip() == "" and st.session_state.is_generating:
            continue

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Chỉ hiển thị feedback cho assistant
            if msg["role"] == "assistant" and msg["content"].strip():
                fb_value = st.session_state.feedback_log.get(i)
                st.session_state[f"feedback_{i}"] = fb_value

                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=fb_value is not None,
                    on_change=save_feedback,
                    args=(i,),
                )


# --- 4. Hiển thị phần chọn model & input ---
def display_chat_controls() -> tuple[Optional[str], str]:
    try:
        model_options = get_ai_response_stream()
    except Exception as e:
        st.error(f"Lỗi khi lấy danh sách model: {e}")
        model_options = ["default-model"]

    selected_model = st.selectbox(
        "Chọn Model:",
        model_options,
        disabled=st.session_state.is_generating,
    )

    c1, c2 = st.columns([10, 1])
    with c1:
        prompt = st.chat_input("Nhập câu hỏi...", disabled=st.session_state.is_generating)
    with c2:
        if st.session_state.is_generating:
            if st.button("⏹", use_container_width=True, type="primary"):
                st.session_state.stop_generation = True
                st.toast("🛑 Dừng")
                st.rerun()

    return prompt, selected_model


# --- 5. Logic gửi prompt ---
def handle_prompt_submission(prompt: str, current_chat: Dict[str, Any]):
    current_chat["messages"].append({"role": "user", "content": prompt})
    current_chat["messages"].append({"role": "assistant", "content": ""})
    st.session_state.is_generating = True


# --- 6. Stream phản hồi ---
def stream_and_display_response(current_chat: Dict[str, Any], selected_model: str):
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        model_name = node_name = None
        user_prompt = current_chat["messages"][-2]["content"]

        try:
            stream = get_ai_response_stream(user_prompt, selected_model, activity="chat")

            for packet in stream:
                if st.session_state.stop_generation:
                    st.toast("Đã dừng")
                    break

                text_chunk = packet.get("content_chunk", "")
                model_name = packet.get("ls_model_name") or model_name
                meta = packet.get("metadata", {})
                node_name = meta.get("langgraph_node") or node_name

                full_response += text_chunk
                header = f"**Model:** `{model_name}` | **Node:** `{node_name}`" if model_name and node_name else ""
                placeholder.markdown(f"{header}\n\n{full_response}▌")

            header = f"**Model:** `{model_name}` | **Node:** `{node_name}`" if model_name and node_name else ""
            placeholder.markdown(f"{header}\n\n{full_response}")

            # ✅ Hiển thị feedback “thumbs” ngay dưới phản hồi cuối
            st.feedback(
                "thumbs",
                key=f"feedback_{len(current_chat['messages'])}",
                on_change=save_feedback,
                args=(len(current_chat["messages"]),),
            )

        except Exception as e:
            st.error(f"Lỗi khi streaming phản hồi: {e}")
            full_response = "Đã xảy ra lỗi, vui lòng thử lại."
            placeholder.markdown(full_response)
        finally:
            current_chat["messages"][-1]["content"] = full_response
            st.session_state.is_generating = False
            st.session_state.stop_generation = False


# --- 7. Hàm chính ---
def render_chat_area():
    st.header("💬 Chat")

    initialize_session_state()

    if not st.session_state.get("current_chat_id") and not st.session_state.get("chat_history"):
        create_new_chat()

    if not st.session_state.get("current_chat_id"):
        st.info("Hãy bắt đầu một chat mới từ sidebar.")
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
