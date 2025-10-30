import streamlit as st

def load_css():
    """Tải tất cả CSS động, tự động thích ứng với Light/Dark Mode."""
    st.markdown("""
<style>
/* CSS này dùng biến của Streamlit, 
nên sẽ tự động đổi màu theo theme (Light/Dark) của người dùng.
*/

/* Đảm bảo các thành phần chính CỐ ĐỊNH CHIỀU RỘNG/DÀI và CÓ PADDING */
section.main, .stApp {
    max-width: 2000px; /* Cố định chiều rộng tối đa */
    min-height: 80vh; /* Cố định chiều DÀI (cao) tối thiểu */
    margin: auto; /* Tự động căn giữa */
    padding: 0 1.5rem; /* Thêm đệm trái/phải để không bị dính cạnh */
}

/* Tin nhắn của User */
.user-msg {
    /* Dùng màu nền chính và viền màu nhấn */
    background-color: var(--streamlit-background-color);
    border: 1px solid var(--streamlit-primary-color);
    color: var(--streamlit-text-color);
    border-radius: 16px;
    padding: 8px 12px; 
    margin: 4px 0 4px 15px; 
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Tin nhắn của Assistant */
.assistant-msg {
    /* Dùng màu nền phụ */
    background-color: var(--streamlit-secondary-background-color);
    color: var(--streamlit-text-color);
    border-radius: 16px;
    padding: 8px 12px; 
    margin: 4px 15px 4px 0; 
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* Activity log styling */
.activity-item {
    /* Dùng màu nền phụ */
    background-color: var(--streamlit-secondary-background-color);
    border-left: 4px solid var(--streamlit-primary-color);
    color: var(--streamlit-text-color);
    padding: 6px 10px; 
    border-radius: 6px;
    margin-bottom: 4px; 
}

/*
--- Tinh chỉnh giao diện chung ---
*/

/* Bo tròn ô nhập text */
textarea {
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 15px !important;
    /* Màu sắc sẽ tự động theo theme */
}

/* Bo tròn ô chọn model */
div[data-baseweb="select"] {
    border-radius: 8px !important;
    background-color: var(--streamlit-secondary-background-color) !important;
    font-size: 13px !important;
    padding: 2px !important;
}
/* Chữ trong ô select */
div[data-baseweb="select"] div {
    /* Màu chữ sẽ tự động theo theme */
    background-color: transparent !important;
}

/* Bo tròn các nút */
button[kind="secondary"], button[kind="primary"] {
    border-radius: 10px !important;
}
.small-pause-btn {
        background-color: #ef4444;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 8px;
        font-size: 13px;
        width: 100%;
        cursor: pointer;
            }
.small-pause-btn:hover {
        background-color: #dc2626;
            }
</style>

""", 
unsafe_allow_html=True)

