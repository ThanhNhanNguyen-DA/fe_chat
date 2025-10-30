import streamlit as st
from datetime import datetime

STYLE = {
    "base_bg": "#f9fafb",
    "border": "#e5e7eb",
    "text_color": "#1e293b",
    "time_color": "#94a3b8",
}

def summarize_activity(activity: dict) -> str:
    """Tóm tắt ngắn gọn hành động theo metadata."""
    action = activity.get("action", "")
    meta = activity.get("metadata", {}) or {}
    node = meta.get("langgraph_node", "")
    model = meta.get("ls_model_name", "")

    if "call_model" in node:
        return f"📡 Đang gửi yêu cầu đến {model or 'mô hình AI'}"
    if "retrieval" in node or "vector" in node:
        return "🔍 Đang truy xuất dữ liệu từ kho tri thức CMC"
    if "embedding" in node:
        return "🧠 Đang tạo vector embedding"
    if "judge" in node:
        return "⚖️ Đang chấm điểm phản hồi mô hình"
    if "summary" in node or "aggregate" in node:
        return "📊 Đang tổng hợp kết quả đánh giá"
    if "Hoàn tất" in action:
        return "✅ Hoàn tất tiến trình"
    if "Lỗi" in action:
        return "❌ Lỗi khi gọi backend"
    return "🔸 " + (action or "Đang xử lý...")

def get_bg_color(summary: str) -> str:
    if "Lỗi" in summary:
        return "#fee2e2"
    if "Hoàn tất" in summary:
        return "#dcfce7"
    if "truy xuất" in summary:
        return "#fef9c3"
    if "gửi yêu cầu" in summary:
        return "#e0f2fe"
    return STYLE["base_bg"]

def render_activity_log():
    """Hiển thị log hoạt động realtime: tự cập nhật khi stream chạy."""
    st.subheader("⚡ Nhật ký hoạt động (Realtime)")

    activities = st.session_state.get("activities", [])
    if not activities:
        st.info("Không có hoạt động nào.")
        return

    for activity in activities:
        summary = summarize_activity(activity)
        bg = get_bg_color(summary)
        time = activity.get("time", datetime.now().strftime("%H:%M:%S"))

        st.markdown(
            f"""
            <div style="
                background:{bg};
                border:1px solid {STYLE['border']};
                border-radius:10px;
                padding:8px 12px;
                margin-bottom:8px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                font-size:13px;
                color:{STYLE['text_color']};
                box-shadow:0 1px 2px rgba(0,0,0,0.05);
                transition:background 0.2s ease;
            ">
                <div>{summary}</div>
                <div style='color:{STYLE['time_color']};font-size:11px'>{time}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
