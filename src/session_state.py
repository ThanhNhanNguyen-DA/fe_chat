import streamlit as st

def init_session_state():
    """Khởi tạo tất cả các biến session state cần thiết."""
    
    # Cấu hình chung
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
        st.session_state.username = ""

    # Lịch sử chat
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = {}
        st.session_state.current_chat_id = None
        st.session_state.chat_counter = 0

    # Log hoạt động
    if 'activities' not in st.session_state:
        st.session_state.activities = []

    # Trạng thái UI
    if 'rename_mode' not in st.session_state:
        st.session_state.rename_mode = None
    if 'share_chat_id' not in st.session_state:
        st.session_state.share_chat_id = None
    
    # Lựa chọn model
    if 'selected_model' not in st.session_state:
        # Bạn có thể thay đổi model mặc định ở đây
        st.session_state.selected_model = "gpt-4o" 
    
    # Cờ này = True khi AI đang trong quá trình stream
    # --- KHỞI TẠO STATE ---
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

    if "stop_generation" not in st.session_state:
        st.session_state.stop_generation = False


