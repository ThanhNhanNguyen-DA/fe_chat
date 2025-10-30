import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_backend_url() -> str:
    """Trả về URL backend (ưu tiên Streamlit secrets -> .env -> localhost)."""
    return (
        getattr(st.secrets, "BACKEND_URL", None)
        or os.getenv("BACKEND_URL", "http://localhost:8000")
    ).rstrip("/")

def get_stream_timeout() -> int:
    """Thời gian timeout stream (mặc định 180s)."""
    return int(os.getenv("STREAM_TIMEOUT", 180))

def build_url(path: str) -> str:
    """Ghép URL backend và path."""
    return f"{get_backend_url()}/{path.lstrip('/')}"

def get_page_config() -> dict:
    """Cấu hình trang chính."""
    return {
        "page_title": os.getenv("APP_NAME", "CMC Q&A"),
        "page_icon": os.getenv("PAGE_ICON", "🤖"),
        "layout": os.getenv("LAYOUT", "wide"),
        "initial_sidebar_state": os.getenv("SIDEBAR_STATE", "expanded"),
    }
