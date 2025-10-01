import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings

# ------------------------------
# Cấu hình
# ------------------------------
DB_PATH = "vectorstores/db_faiss"
EMBED_MODEL_PATH = "models/all-MiniLM-L6-v2-f16.gguf"
DATA_DIR = "data"
METADATA_FILE = os.path.join(DB_PATH, "metadata.txt")

# ------------------------------
# Load hoặc khởi tạo DB
# ------------------------------
def load_vector_db():
    embeddings = GPT4AllEmbeddings(model_file=EMBED_MODEL_PATH)
    if os.path.exists(DB_PATH):
        return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return FAISS.from_documents([], embeddings)

# ------------------------------
# Lưu DB
# ------------------------------
def save_vector_db(db):
    db.save_local(DB_PATH)

# ------------------------------
# Thêm tài liệu từ 1 file
# ------------------------------
def add_documents(filepath):
    # chọn loader phù hợp
    if filepath.endswith(".txt"):
        loader = TextLoader(filepath, encoding="utf-8")
    elif filepath.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
    else:
        raise ValueError("Unsupported file type")

    # load tài liệu
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    # load db
    db = load_vector_db()
    db.add_documents(docs)

    # lưu lại DB
    save_vector_db(db)

    # lưu metadata (danh sách file đã nạp)
    os.makedirs(DB_PATH, exist_ok=True)
    with open(METADATA_FILE, "a", encoding="utf-8") as f:
        f.write(os.path.basename(filepath) + "\n")

    return True

# ------------------------------
# Thêm toàn bộ file trong thư mục data
# ------------------------------
def create_db_from_files():
    loader = DirectoryLoader(DATA_DIR, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = GPT4AllEmbeddings(model_file=EMBED_MODEL_PATH)
    db = FAISS.from_documents(chunks, embeddings)

    save_vector_db(db)
    return db

# ------------------------------
# Lấy metadata (danh sách file đã nạp)
# ------------------------------
def get_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return []
