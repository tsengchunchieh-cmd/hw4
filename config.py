"""
Configuration module for RAG application
Handles environment variables and default settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# API Configuration
# ============================================================================

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")


# ============================================================================
# Model Configuration
# ============================================================================

# EmbeddingGemma Configuration
EMBEDDING_MODEL_NAME = "google/embeddinggemma-300m"
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")
EMBEDDING_NORMALIZE = True

# Gemini Configuration
LLM_MODEL_NAME = "gemini-2.5-flash"
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))


# ============================================================================
# Text Processing Configuration
# ============================================================================

# Text Splitter
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

# Retriever
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "4"))


# ============================================================================
# File and Directory Configuration
# ============================================================================

# Database paths
FAISS_DB_PATH = os.getenv("FAISS_DB_PATH", "faiss_db")
TEMP_UPLOAD_DIR = os.getenv("TEMP_UPLOAD_DIR", "uploaded_docs")

# Supported file extensions
SUPPORTED_FILE_TYPES = ["pdf", "txt", "docx"]
MAX_FILE_SIZE_MB = 100  # Maximum file size in MB


# ============================================================================
# Prompts and Templates
# ============================================================================

RAG_SYSTEM_PROMPT = """
作為一個樂於助人的問答機器人，請根據提供的上下文 (Context) 來回答問題 (Question)。
如果你無法從上下文中找到答案，請誠實地回答「根據提供的資料，我無法回答這個問題。」
請使用繁體中文回答。
"""

RAG_PROMPT_TEMPLATE = """
作為一個樂於助人的問答機器人，請根據提供的上下文 (Context) 來回答問題 (Question)。
如果你無法從上下文中找到答案，請誠實地回答「根據提供的資料，我無法回答這個問題。」
請使用繁體中文回答。

Context:
{context}

Question:
{question}
"""


# ============================================================================
# UI Configuration
# ============================================================================

# Streamlit Page Configuration
PAGE_TITLE = "📚 RAG 文件問答系統"
PAGE_ICON = "📚"
PAGE_LAYOUT = "wide"

# Tab Names
TAB_DATABASE = "📤 建立資料庫"
TAB_QUESTION = "❓ 提問"


# ============================================================================
# Error Messages (Traditional Chinese)
# ============================================================================

ERROR_NO_FILES = "請先選擇至少一個文件。"
ERROR_NO_TOKEN = "請輸入 HuggingFace Token。"
ERROR_NO_API_KEY = "請輸入 Google API Key。"
ERROR_NO_DATABASE = "請先建立或載入向量資料庫。"
ERROR_CREATE_DB = "❌ 建立資料庫時出錯：{}"
ERROR_LOAD_DB = "❌ 載入資料庫時出錯：{}"
ERROR_SAVE_DB = "❌ 保存資料庫時出錯：{}"
ERROR_QUERY = "❌ 執行查詢時出錯：{}"
ERROR_EMPTY_QUERY = "⚠️ 請輸入問題。"

# Success Messages
SUCCESS_DB_CREATED = "✅ 向量資料庫建立成功！"
SUCCESS_DB_SAVED = "✅ 資料庫已保存！"
SUCCESS_DB_LOADED = "✅ 資料庫載入成功！"

# Warning Messages
WARNING_NO_API_KEY = "⚠️ 請在側邊欄輸入 Google API Key。"
WARNING_DB_NOT_READY = "⚠️ 請先建立向量資料庫。"
WARNING_NO_DOCUMENTS = "ℹ️ 未檢索到相關文件片段。"

# Info Messages
INFO_SUPPORTED_FORMATS = """
### 支持的文件格式
- **PDF** (.pdf)
- **Word 文件** (.docx)
- **純文字** (.txt)
"""

INFO_NO_DB_FOUND = "ℹ️ 未找到已保存的資料庫。請先建立新資料庫。"
INFO_LOAD_EXISTING = "ℹ️ 資料庫未準備好，請先建立或載入。"
INFO_UPLOAD_FIRST = "ℹ️ 請先在「建立資料庫」標籤中建立或載入向量資料庫。"


# ============================================================================
# Utility Functions
# ============================================================================

def validate_api_keys():
    """
    Validate that required API keys are configured.
    
    Returns:
        tuple: (is_valid, missing_keys)
    """
    missing_keys = []
    
    if not HUGGINGFACE_TOKEN:
        missing_keys.append("HUGGINGFACE_TOKEN")
    
    if not GOOGLE_API_KEY:
        missing_keys.append("GOOGLE_API_KEY")
    
    return len(missing_keys) == 0, missing_keys


def get_config_summary():
    """
    Get a summary of current configuration.
    
    Returns:
        dict: Configuration summary
    """
    return {
        "embedding_model": EMBEDDING_MODEL_NAME,
        "llm_model": LLM_MODEL_NAME,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "retriever_k": RETRIEVER_K,
        "supported_formats": SUPPORTED_FILE_TYPES,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "database_path": FAISS_DB_PATH,
    }


if __name__ == "__main__":
    # Print configuration summary when run as script
    import json
    print("RAG Application Configuration:")
    print(json.dumps(get_config_summary(), indent=2, ensure_ascii=False))
