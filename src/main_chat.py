import streamlit as st
import requests
from src.api import get_ai_response_stream
from src.chat_utils import create_new_chat, log_ai_activity

COLORS = {
    "bg_user": "#e2e8f0",
    "bg_assistant": "#f1f5f9",
    "border": "#cbd5e1",
    "text": "#1e293b",
    "accent": "#3b82f6",
}


def render_chat_area():
    """Khung chat realtime (bo góc, màu dịu)."""
    st.header("💬 Chat")

    # --- INIT STATE ---
    for key, val in {
        "is_generating": False,
        "stop_generation": False,
        "activities": [],
    }.items():
        st.session_state.setdefault(key, val)

    if not st.session_state.current_chat_id and not st.session_state.chat_history:
        create_new_chat()

    if not st.session_state.current_chat_id:
        st.info("Hãy bắt đầu một chat mới từ sidebar.")
        return

    current_chat = st.session_state.chat_history[st.session_state.current_chat_id]

    # --- HIỂN THỊ LỊCH SỬ ---
    chat_container = st.container(height=420)
    with chat_container:
        for msg in current_chat["messages"]:
            bg = COLORS["bg_user"] if msg["role"] == "user" else COLORS["bg_assistant"]
            role = "👤 Bạn" if msg["role"] == "user" else "🤖 Trợ lý"
            st.markdown(
                f"""
                <div style="
                    background:{bg};
                    color:{COLORS['text']};
                    border:1px solid {COLORS['border']};
                    border-radius:12px;
                    padding:10px 14px;
                    margin-bottom:10px;">
                    <b>{role}:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- MODEL HIỆN TẠI ---
    def fetch_current_model():
        try:
            res = requests.get("http://localhost:8000/current-model", timeout=5)
            return res.json().get("model", "Không có model") if res.status_code == 200 else "Không có model"
        except Exception as e:
            st.warning(f"Lỗi khi lấy model: {e}")
            return "Không có model"

    st.session_state.setdefault("selected_model", fetch_current_model())
    st.selectbox("### 🧠 Model hiện tại:", [st.session_state.selected_model], index=0, disabled=True)

    # --- INPUT + STOP ---
    c1, c2 = st.columns([10, 1])
    with c1:
        prompt = st.chat_input("Nhập câu hỏi...", disabled=st.session_state.is_generating)
    with c2:
        if st.session_state.is_generating and st.button("⏹", use_container_width=True, type="primary"):
            st.session_state.stop_generation = True
            st.toast("🛑 Dừng tiến trình")

    if not prompt or st.session_state.is_generating:
        return

    # --- GỬI CÂU HỎI ---
    current_chat["messages"].append({"role": "user", "content": prompt})
    st.session_state.is_generating = True

    with chat_container:
        st.markdown(
            f"""
            <div style="
                background:{COLORS['bg_user']};
                color:{COLORS['text']};
                border:1px solid {COLORS['border']};
                border-radius:12px;
                padding:10px 14px;
                margin-bottom:10px;">
                <b>👤 Bạn:</b> {prompt}
            </div>
            """,
            unsafe_allow_html=True,
        )

    def stream_response():
        full_text = ""
        model_name = None
        for packet in get_ai_response_stream(prompt, st.session_state.selected_model, "chat"):
            if st.session_state.stop_generation:
                log_ai_activity("🛑 Dừng tiến trình", "Người dùng nhấn Stop.")
                break

            text = packet.get("content_chunk", "")
            if not text:
                continue

            meta = packet.get("metadata", {})
            node = meta.get("langgraph_node", "?")
            model_name = meta.get("ls_model_name") or st.session_state.selected_model

            full_text += text
            log_ai_activity("📡 Chunk mới", f"Node: {node} | Model: {model_name}", meta)
            yield text

        log_ai_activity("✅ Hoàn tất tiến trình", f"Mô hình: {model_name or st.session_state.selected_model}")

    with chat_container:
        st.markdown(
            f"""
            <div style="
                background:{COLORS['bg_assistant']};
                color:{COLORS['text']};
                border:1px solid {COLORS['border']};
                border-radius:12px;
                padding:10px 14px;
                margin-bottom:10px;">
                <b>🤖 Trợ lý:</b> """,
            unsafe_allow_html=True,
        )
        full_reply = st.write_stream(stream_response())
        st.markdown("</div>", unsafe_allow_html=True)

    current_chat["messages"].append({"role": "assistant", "content": full_reply})
    st.session_state.is_generating = False
    st.session_state.stop_generation = False
