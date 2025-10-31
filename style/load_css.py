import streamlit as st

def load_css():
    """Tải CSS cho toàn bộ app (sidebar + chat + activity + chat_input luôn hiển thị)."""
    st.markdown("""
    <style>
    /* === TOÀN BỘ APP === */
    html, body, .stApp {
        background-color: #262730 !important;
        color: #ffffff !important;
    }

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0078D7 0%, #005EB8 100%) !important;
        color: #ffffff !important;
        border-right: 2px solid rgba(0, 0, 0, 0.4);
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] button {
        background-color: #0A84FF !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #4CB2FF !important;
        transition: all 0.25s ease-in-out;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #38A3FF !important;
        transform: scale(1.03);
        box-shadow: 0 0 10px rgba(56,163,255,0.6);
    }

    /* === HEADER === */
    [data-testid="stHeader"] {
        background-color: #262730 !important;
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* === KHUNG CHAT === */
    .stChatMessage {
        background-color: #1f2024 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        padding: 10px !important;
    }

    /* === ANIMATION viền sáng xung nhịp === */
    @keyframes pulse-blue {
        0%   { box-shadow: 0 0 10px rgba(0,120,215,0.4); }
        50%  { box-shadow: 0 0 22px rgba(76,178,255,1); }
        100% { box-shadow: 0 0 10px rgba(0,120,215,0.4); }
    }

    /* === Ô NHẬP CÂU HỎI: LUÔN CÓ BORDER + SHADOW === */
    section[data-testid="stChatInput"] {
        background-color: #1f2024 !important;
        border: 1.8px solid #0078D7 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-top: 10px !important;
        margin-bottom: 8px !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 8px rgba(0, 120, 215, 0.3) !important; /* ✅ luôn hiển thị */
    }

    /* Hover/Focus — sáng hơn */
    section[data-testid="stChatInput"]:hover,
    section[data-testid="stChatInput"]:focus-within {
        border-color: #4cb2ff !important;
        box-shadow: 0 0 16px rgba(76,178,255,0.8) !important;
        background-color: #25272b !important;
    }

    /* Khi AI đang phản hồi (glow-active) */
    .glow-active {
        border-color: #4cb2ff !important;
        animation: pulse-blue 1.8s infinite ease-in-out !important;
    }

    /* === Textarea === */
    section[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #e2e8f0 !important;
        font-size: 16px !important;
        padding: 8px 10px !important;
        border: none !important;
        outline: none !important;
    }

    /* === NÚT GỬI (➤) === */
    button[data-testid="stChatInputSubmit"] {
        color: #60a5fa !important;
        transition: all 0.25s ease-in-out;
    }
    button[data-testid="stChatInputSubmit"]:hover {
        color: #93c5fd !important;
        transform: scale(1.15);
    }

    /* === SELECTBOX (CHỌN MODEL) === */
    div[data-baseweb="select"] > div {
        background-color: #1f2024 !important;
        border: 1.5px solid #0078D7 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 4px 10px !important;
        transition: 0.3s ease-in-out;
    }
    div[data-baseweb="select"]:focus-within > div {
        border-color: #4cb2ff !important;
        box-shadow: 0 0 10px rgba(76,178,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)
