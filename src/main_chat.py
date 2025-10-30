import streamlit as st
from src.api import get_ai_response_stream
from src.chat_utils import create_new_chat

def render_chat_area():
    """Khu vực chat chính với streaming phản hồi."""
    st.header("💬 Chat")

    # Khởi tạo state
    state = st.session_state
    for key, default in {
        "is_generating": False,
        "stop_generation": False,
    }.items():
        state.setdefault(key, default)

    # Kiểm tra chat hiện tại
    if not state.current_chat_id and not state.chat_history:
        create_new_chat()

    if not state.current_chat_id:
        st.info("Hãy bắt đầu chat mới ở sidebar.")
        return

    chat = state.chat_history[state.current_chat_id]
    chat_container = st.container(height=400)
    with chat_container:
        for msg in chat["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chọn model
    models = get_ai_response_stream()
    selected_model = st.selectbox(
        "Chọn Model:", models, key="selected_model", disabled=state.is_generating
    )

    # Input và Stop
    c1, c2 = st.columns([10, 1])
    with c1:
        prompt = st.chat_input("Nhập câu hỏi...", disabled=state.is_generating)
    with c2:
        if state.is_generating and st.button("⏹", use_container_width=True, type="primary"):
            state.stop_generation = True
            st.toast("🛑 Dừng tiến trình")
            st.rerun()

    # Gửi câu hỏi
    if prompt and not state.is_generating:
        chat["messages"] += [{"role": "user", "content": prompt}, {"role": "assistant", "content": ""}]
        state.is_generating = True
        st.rerun()

    # Nhận phản hồi
    if state.is_generating and not state.stop_generation:
        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full, model_name, node_name = "", None, None
                for packet in get_ai_response_stream(prompt, selected_model, activity="chat"):
                    if state.stop_generation:
                        break
                    text = packet.get("content_chunk", "")
                    model_name = packet.get("ls_model_name") or model_name
                    node_name = packet.get("metadata", {}).get("langgraph_node") or node_name
                    full += text
                    placeholder.markdown(
                        f"**Model:** `{model_name}` | **Node:** `{node_name}`\n\n{full}▌"
                    )
                placeholder.markdown(
                    f"**Model:** `{model_name}` | **Node:** `{node_name}`\n\n{full}"
                )
        chat["messages"][-1]["content"] = full
        state.is_generating = state.stop_generation = False
        st.rerun()
