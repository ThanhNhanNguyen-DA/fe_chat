import uuid
import streamlit as st

def login():
    # Customer login form as sidebar and enable session tabs only when the username is entered
    # user chưa xác nhận điều khoản thì không được vào trang chủ
    if "acknowledged" not in st.session_state:
        st.session_state.acknowledged = False

    # tạo sidebar bên trái
    with st.sidebar:
        # tạo cột logo và cột rỗng tỉ lệ 30:1
        logo_col, _ = st.columns([30, 1])

        with logo_col:
            st.title("SA SRE Agent Gen App")
            st.title("Xác nhận")

            # tạo checkbox để user xác nhận điều khoản
            acknowledged = st.checkbox(
                "Tôi xác nhận đã đọc cảnh báo và đồng ý với các điều khoản sử dụng",
                key="acknowledged",
                label_visibility="visible",
            )
            # nếu user chưa đăng nhập thì hiển thị button đăng nhập
            # nút này bị vô hiệu hóa khi user chưa xác nhận điều khoản
            if not st.user.is_logged_in:
                submit = st.button(
                    "Vui lòng đăng nhập trước khi sử dụng",
                    disabled=not (acknowledged),
                )
                # nếu user click vào nút đăng nhập thì đăng nhập với provider microsoft
                if submit:
                    st.login("microsoft")

            if st.user.is_logged_in:
                st.session_state.conversation_id = str(uuid.uuid4())
                st.session_state.user_authenticated = True
                st.session_state.ask_user = True
                st.session_state.isEnabledPrompt = True


                st.rerun()

    # Description and Disclaimer
    # Main page content
    st.markdown(
        "<h1 style='text-align: center;'>Welcome to LLM Evaluator</h1>",
        unsafe_allow_html=True,
    )

    # Description section
    st.header("Description")
    st.write(
        """
    LLM Evaluator là ứng dụng hỗ trợ đánh giá mô hình ngôn ngữ (LLM), giúp bạn so sánh prompt, cấu hình mô hình và phiên bản hệ thống theo nhiều tiêu chí như: chất lượng, tính đúng sự thật, an toàn, chi phí và độ trễ.

    Với LLM Evaluator, bạn có thể:
    - Tạo bộ dữ liệu kiểm thử và kịch bản đánh giá nhất quán.
    - Thiết lập rubric để chấm điểm tự động hoặc so sánh cặp (pairwise).
    - Theo dõi kết quả bằng báo cáo/tổng hợp và xuất dữ liệu (CSV/JSON).
    - Lặp lại thí nghiệm để đảm bảo tính khách quan và so sánh giữa nhiều nhà cung cấp/mô hình.

    Dù bạn là nhà nghiên cứu hay kỹ sư sản phẩm, LLM Evaluator giúp đánh giá LLM một cách hệ thống, minh bạch và có thể tái lập.
    """
    )

    # Add some space between sections
    st.markdown("---")

    # Phần cảnh báo (Disclaimer)
    st.header("Cảnh báo & Điều khoản sử dụng")
    st.write(
        """
- **Nội dung do AI tạo ra:** Ứng dụng LLM Evaluator có thể sử dụng trí tuệ nhân tạo để tạo hoặc chấm điểm phản hồi. Chúng tôi nỗ lực đảm bảo độ chính xác, tuy nhiên thông tin có thể chưa đầy đủ, cập nhật hoặc có sai sót.
- **Không thay thế tư vấn chuyên môn:** Các kết quả/đề xuất từ LLM Evaluator không phải là tư vấn chuyên môn, pháp lý, tài chính hoặc y tế.
- **Có thể tồn tại thiên kiến:** Dữ liệu huấn luyện hay thuật toán có thể tạo ra thiên kiến trong phản hồi hoặc điểm số.
- **Quyền riêng tư & sử dụng dữ liệu:** Tương tác và dữ liệu đánh giá có thể được ghi lại để cải thiện chất lượng dịch vụ.
- **Không đảm bảo về hiệu suất:** Không cam kết truy cập liên tục hoặc vận hành không lỗi cho ứng dụng.
- **Miễn trừ trách nhiệm:** Chúng tôi không chịu trách nhiệm cho bất kỳ thiệt hại hoặc tổn thất nào phát sinh từ việc sử dụng kết quả đánh giá.
- **Trách nhiệm người dùng:** Người dùng tự đánh giá mức độ phù hợp/chính xác của kết quả cho nhu cầu thực tế.
- **Quyền sở hữu trí tuệ:** Không sử dụng kết quả để vi phạm quyền sở hữu trí tuệ.
- **Cập nhật điều khoản:** Điều khoản có thể được cập nhật định kỳ.
- **Các kết quả đánh giá chỉ mang tính tham khảo, cần xem xét bối cảnh ứng dụng cụ thể.**
- **Mọi gợi ý/đề xuất cần được kiểm tra kỹ trước khi áp dụng vào sản phẩm thực tế.**
- **Cần đánh giá chi phí vận hành mô hình trước khi triển khai.**
- **Công cụ này hỗ trợ đánh giá LLM, không thay thế cho quy trình kiểm thử và thẩm định đầy đủ.**

Bằng việc sử dụng LLM Evaluator, bạn xác nhận đã đọc, hiểu và đồng ý với các điều khoản trên.
        """
    )