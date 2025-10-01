import gradio as gr
from simplechain import get_answer as simple_answer
from qabot import get_answer as rag_answer
from prepare_vector_db import add_documents, get_metadata

# ------------------------------
# 🔁 Hàm xử lý chat
# ------------------------------

def chat_simple(message, history):
    """Chat bình thường không dùng RAG"""
    return simple_answer(message)

def chat_rag(message, history):
    """Chat có kiến thức từ tài liệu (RAG)"""
    return rag_answer(message)

# ------------------------------
# 📂 Hàm upload file
# ------------------------------
def upload_files(files):
    added = []
    for file in files:
        add_documents(file.name)
        added.append(file.name)
    meta = get_metadata()
    return f"✅ Đã thêm {len(added)} file mới:\n- " + "\n- ".join(added) + f"\n📚 Tổng số tài liệu hiện có: {len(meta)}"

# ------------------------------
# 📱 Giao diện Gradio
# ------------------------------
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## 🤖 Chatbot LLM + RAG + Upload tài liệu")

    with gr.Tab("💬 Chat thường (không RAG)"):
        gr.ChatInterface(
            fn=chat_simple,
            type="messages",
            title="Chat thường",
            description="Trả lời từ mô hình LLM gốc mà không dùng kiến thức ngoài."
        )

    with gr.Tab("📚 Chat có kiến thức (RAG)"):
        gr.ChatInterface(
            fn=chat_rag,
            type="messages",
            title="Chat RAG",
            description="Sử dụng kiến thức từ tài liệu đã upload để trả lời chính xác hơn."
        )

    with gr.Tab("📂 Quản lý tài liệu"):
        gr.Markdown("### 📁 Upload tài liệu để mở rộng kiến thức")
        file_input = gr.File(
            file_types=[".txt", ".pdf"],
            label="Chọn tài liệu",
            file_count="multiple"
        )
        upload_btn = gr.Button("🚀 Cập nhật kiến thức")
        upload_output = gr.Textbox(label="📜 Kết quả cập nhật")

        upload_btn.click(upload_files, inputs=[file_input], outputs=[upload_output])

demo.launch(server_name="0.0.0.0", server_port=7860)
