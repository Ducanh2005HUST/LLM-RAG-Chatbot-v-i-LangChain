=========================================================
🚀 HƯỚNG DẪN CÀI ĐẶT & CHẠY CHATBOT HỖ TRỢ TÀI LIỆU TRONG CÔNG TY
=========================================================

1️⃣ YÊU CẦU HỆ THỐNG
-----------------------------------------
- Python >= 3.10 (khuyến nghị 3.10 hoặc 3.11)
- pip >= 22
- Máy tính có RAM >= 8GB (tùy model bạn chạy)
- Đã tải 2 model GGUF (LLaMA, Embedding) về thư mục `models/`
- Link tải 2 model: https://huggingface.co/vilm/vinallama-7b-chat
- https://huggingface.co/caliex/all-MiniLM-L6-v2-f16.gguf


-----------------------------------------

2️⃣ CÀI ĐẶT THƯ VIỆN
-----------------------------------------
Chạy lệnh sau trong terminal (MacOS/Linux) hoặc PowerShell (Windows):

    pip install -r requirements.txt

Nếu chưa có `requirements.txt`, hãy copy nội dung sau:

    gradio
    langchain
    langchain-community
    faiss-cpu
    ctransformers
    pypdf

-----------------------------------------

3️⃣ CHUẨN BỊ DỮ LIỆU
-----------------------------------------
- Tạo thư mục `data/` để chứa file PDF hoặc TXT bạn muốn cho chatbot học
- Tạo thư mục `vectorstores/` để lưu FAISS database
- Tạo thư mục `models/` để lưu LLM + embedding model

Cấu trúc ví dụ:
    .
    ├── app.py
    ├── qabot.py
    ├── simplechain.py
    ├── prepare_vector_db.py
    ├── data/                # file PDF, TXT upload
    ├── vectorstores/        # FAISS DB lưu tri thức
    └── models/              # chứa GGUF model

-----------------------------------------

4️⃣ CHẠY ỨNG DỤNG
-----------------------------------------
Khởi động chatbot bằng:

    python app.py

Nếu chạy thành công, bạn sẽ thấy log kiểu:

    Running on local URL:  http://127.0.0.1:7860

Mở trình duyệt và truy cập link đó.

-----------------------------------------

5️⃣ SỬ DỤNG
-----------------------------------------
- Tab 💬 Chat thường: Chat trực tiếp với LLM
- Tab 📚 Chat có kiến thức: Chat dựa trên tri thức đã upload
- Tab 📂 Quản lý tài liệu: Upload file mới (txt/pdf) để mở rộng DB

-----------------------------------------

6️⃣ NOTE
-----------------------------------------
- Vector DB được lưu trong thư mục `vectorstores/db_faiss`, nên lần sau mở app vẫn giữ tri thức cũ.
- Nếu muốn reset toàn bộ DB: chỉ cần xóa thư mục `vectorstores/db_faiss`.

