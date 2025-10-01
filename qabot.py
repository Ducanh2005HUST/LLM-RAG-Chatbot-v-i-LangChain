from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

# ------------------------------
# Cấu hình
# ------------------------------
MODEL_PATH = "models/vinallama-7b-chat_q5_0.gguf"
EMBEDDING_MODEL_PATH = "models/all-MiniLM-L6-v2-f16.gguf"
VECTOR_DB_PATH = "vectorstores/db_faiss"

# ------------------------------
# Load LLM
# ------------------------------
def load_llm(model_file: str):
    return CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )

# ------------------------------
# Tạo prompt template
# ------------------------------
def create_prompt():
    template = """<|im_start|>system
Sử dụng thông tin sau đây để trả lời câu hỏi. 
Nếu bạn không biết câu trả lời, hãy nói "Tôi không biết", đừng bịa ra.
{context}<|im_end|>
<|im_start|>user
{question}<|im_end|>
<|im_start|>assistant"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

# ------------------------------
# Load Vector DB
# ------------------------------
def load_vector_db():
    embeddings = GPT4AllEmbeddings(model_file=EMBEDDING_MODEL_PATH)
    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

# ------------------------------
# Hàm trả lời
# ------------------------------
def get_answer(question: str) -> str:
    db = load_vector_db()
    llm = load_llm(MODEL_PATH)
    prompt = create_prompt()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False,
        chain_type_kwargs={'prompt': prompt}
    )

    result = qa.invoke({"query": question})
    return result.get("result", str(result))
