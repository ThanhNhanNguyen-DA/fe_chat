import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, Generator
import streamlit as st

STYLE = {
    "bg": "#1e293b",
    "border": "#334155",
    "text": "#f1f5f9",
    "time": "#94a3b8",
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


def format_log(log: Dict[str, Any]) -> str:
    """Format HTML 1 dòng log (dark theme)."""
    return f"""
    <div style='background:{STYLE["bg"]};
                border:1px solid {STYLE["border"]};
                border-radius:10px;
                padding:8px 10px;
                margin-bottom:6px;
                color:{STYLE["text"]};
                font-size:13px;'>
        <b>{log['action']}</b> — {log.get('details', '')}
        <span style='float:right;color:{STYLE["time"]};
                     font-size:11px'>{log.get('time', '')}</span>
    </div>
    """


def log_ai_activity(action: str, details: str = "", metadata=None):
    """Ghi log (Producer)."""
    entry = ActivityEntry.create(action, details, metadata)
    st.session_state.setdefault("activities", [])
    st.session_state.activities.append(asdict(entry))


def activity_stream() -> Generator[str, None, None]:
    """Stream log realtime từ session_state."""
    if "activities" not in st.session_state:
        st.session_state["activities"] = []

    last_len = len(st.session_state["activities"])
    while st.session_state.get("is_generating", False):
        logs = st.session_state["activities"]
        if len(logs) > last_len:
            for log in logs[last_len:]:
                yield format_log(log)
            last_len = len(logs)
        time.sleep(0.1)

    # Kiểm tra sót log cuối
    logs = st.session_state["activities"]
    for log in logs[last_len:]:
        yield format_log(log)


def render_activity_log():
    """UI phần log realtime (dark mode)."""
    st.markdown("### ⚡ Hoạt động realtime")
    st.session_state.setdefault("activities", [])

    log_container = st.container(height=420, border=False)
    with log_container:
        for log in st.session_state["activities"][-8:]:
            st.markdown(format_log(log), unsafe_allow_html=True)

    if st.session_state.get("is_generating", False):
        with log_container:
            st.write_stream(activity_stream())
