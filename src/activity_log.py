import streamlit as st
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Generator
import time

# -----------------------------
# 🎨 STYLE
# -----------------------------
STYLE = {
    "bg": "#1e293b",
    "border": "#334155",
    "text": "#f1f5f9",
    "time": "#94a3b8",
    "thinking_bg": "#0ea5e9",
}



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


def log_ai_activity(action: str, details: str = "", metadata=None):
    """Ghi 1 log mới vào session."""
    entry = ActivityEntry.create(action, details, metadata)
    st.session_state.setdefault("activities", [])
    st.session_state.activities.append(asdict(entry))


def format_log_html(log: Dict[str, Any]) -> str:
    """Trả về HTML format đẹp cho 1 dòng log."""
    meta = log.get("metadata", {}) or {}
    node = meta.get("langgraph_node", "-")
    step = meta.get("langgraph_step", "-")
    thread = meta.get("thread_id", "-")

    return f"""
    <div style='background:{STYLE["bg"]};
                border:1px solid {STYLE["border"]};
                border-radius:10px;
                padding:8px 10px;
                margin-bottom:6px;
                color:{STYLE["text"]};
                font-size:13px;'>
        <b>{log['action']}</b> — {log.get('details','')}
        <span style='float:right;color:{STYLE["time"]};
                     font-size:11px'>{log['time']}</span>
        <div style='font-size:11px;color:{STYLE["time"]};
                    margin-top:4px;'>
            Node: <b>{node}</b> | Step: {step} | Thread: {thread}
        </div>
    </div>
    """


# -----------------------------
# ⚡ ACTIVITY LOG (stream + toggle)
# -----------------------------
def render_activity_log():
    """Hiển thị log realtime + reasoning + toggle."""
    st.markdown("### ⚡ Activity")

    st.session_state.setdefault("activities", [])
    st.session_state.setdefault("show_activity", True)

    # 🔘 Toggle button
    toggle_label = "Ẩn " if st.session_state.show_activity else "Hiện "
    if st.button(f"👁 {toggle_label}", key="toggle_activity", use_container_width=True):
        st.session_state.show_activity = not st.session_state.show_activity
        st.rerun()

    # --- CSS animation ---
    st.markdown("""
        <style>
        .slide-container {
            overflow: hidden;
            max-height: 0;
            opacity: 0;
            transition: max-height 0.6s ease, opacity 0.4s ease;
        }
        .slide-container.show {
            max-height: 1200px;
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.show_activity:
        st.markdown("<div class='slide-container'></div>", unsafe_allow_html=True)
        return

    st.markdown("<div class='slide-container show'>", unsafe_allow_html=True)

    placeholder = st.empty()
    think_container = st.empty()
    expander_placeholder = st.empty()

    # ---------------------
    # STREAM LOG GENERATOR
    # ---------------------
    def stream_activity() -> Generator[None, None, None]:
        think_mode = False
        think_content = ""
        think_start = None

        for log in st.session_state.get("activities", []):
            meta = log.get("metadata", {}) or {}
            node = meta.get("langgraph_node", "").lower()

            # 🧠 Nếu là reasoning node
            if "thinking" in node:
                if not think_mode:
                    think_mode = True
                    think_start = time.time()
                    think_container.markdown(
                        f"<div style='background:{STYLE['thinking_bg']};"
                        f"padding:8px;border-radius:6px;color:white;'>🧠 <b>Đang suy nghĩ...</b></div>",
                        unsafe_allow_html=True,
                    )
                think_content += log["details"] + "\n"
                think_container.markdown(
                    f"<div style='background:{STYLE['thinking_bg']};padding:8px;"
                    f"border-radius:6px;color:white;'>🧠 <b>Đang suy nghĩ...</b><br>{think_content}</div>",
                    unsafe_allow_html=True,
                )

            else:
                # Nếu thoát reasoning phase → collapse reasoning lại
                if think_mode:
                    think_mode = False
                    duration = time.time() - (think_start or time.time())
                    think_container.empty()
                    with expander_placeholder.expander(
                        f"🧩 Quá trình suy nghĩ (tổng {duration:.2f}s)"
                    ):
                        st.text(think_content)
                    think_content = ""

                placeholder.markdown(format_log_html(log), unsafe_allow_html=True)
            yield  # Cho phép write_stream update UI

        # Nếu reasoning còn đang mở mà stream kết thúc
        if think_mode:
            think_mode = False
            duration = time.time() - (think_start or time.time())
            think_container.empty()
            with expander_placeholder.expander(
                f"🧩 Quá trình suy nghĩ (tổng {duration:.2f}s)"
            ):
                st.text(think_content)

    # ---------------------
    # STREAM UI
    # ---------------------
    st.write_stream(stream_activity())

    st.markdown("</div>", unsafe_allow_html=True)
