import streamlit as st
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx
from src.api import get_ai_response_stream
from src.chat_utils import create_new_chat, log_ai_activity

def render_chat_area():
    """Hiển thị chat và stream phản hồi theo thời gian thực bằng thread."""
    st.header("💬 Chat")

    # --- Init state ---
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "stop_generation" not in st.session_state:
        st.session_state.stop_generation = False

    if not st.session_state.current_chat_id and not st.session_state.chat_history:
        create_new_chat()

    if not st.session_state.current_chat_id:
        st.info("Hãy bắt đầu một chat mới từ sidebar.")
        return

    current_chat = st.session_state.chat_history[st.session_state.current_chat_id]

    chat_container = st.container(height=400)
    with chat_container:
        for msg in current_chat["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # --- Model Selection ---
    model_options = get_ai_response_stream()
    selected_model = st.selectbox(
        "Chọn Model:", model_options, disabled=st.session_state.is_generating
    )

    # --- Input + Stop ---
    c1, c2 = st.columns([10, 1])
    with c1:
        prompt = st.chat_input("Nhập câu hỏi...", disabled=st.session_state.is_generating)
    with c2:
        if st.session_state.is_generating:
            if st.button("⏹", use_container_width=True, type="primary"):
                st.session_state.stop_generation = True
                st.toast("🛑 Dừng tiến trình")

    # --- Gửi câu hỏi ---
    if prompt and not st.session_state.is_generating:
        current_chat["messages"].append({"role": "user", "content": prompt})
        current_chat["messages"].append({"role": "assistant", "content": ""})
        st.session_state.is_generating = True

        placeholder = st.empty()

        def stream():
            full = ""
            model_name = node_name = None
            for packet in get_ai_response_stream(prompt, selected_model, activity="chat"):
                if st.session_state.stop_generation:
                    break

                text = packet.get("content_chunk", "")
                model_name = packet.get("ls_model_name") or model_name
                meta = packet.get("metadata", {})
                node_name = meta.get("langgraph_node") or node_name
                full += text

                header = (
                    f"**Model:** `{model_name}` | **Node:** `{node_name}`"
                    if model_name and node_name
                    else ""
                )
                placeholder.markdown(f"{header}\n\n{full}▌")
                log_ai_activity(
                    "📡 Stream chunk hiển thị", f"Node {node_name} - Model {model_name}"
                )

            placeholder.markdown(
                f"**Model:** `{model_name}` | **Node:** `{node_name}`\n\n{full}"
            )
            current_chat["messages"][-1]["content"] = full
            st.session_state.is_generating = False
            st.session_state.stop_generation = False

        t = threading.Thread(target=stream)
        add_script_run_ctx(t)
        t.start()
