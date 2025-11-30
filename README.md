# 📚 RAG 文件問答系統 - 使用指南

## 🎯 項目概述

這是一個完整的 **Retrieval-Augmented Generation (RAG)** 文件問答系統，結合了以下技術：

- **向量化模型**: Google EmbeddingGemma-300m
- **LLM**: Google Gemini 2.5 Flash
- **框架**: LangChain + Streamlit
- **向量資料庫**: FAISS
- **支持格式**: PDF、DOCX、TXT

## 📋 系統架構

```
streamlit_app.py (主應用)
    ├── embeddings.py (EmbeddingGemma 類別)
    ├── rag_chain.py (RAG 查詢管道)
    └── vector_store.py (向量資料庫管理)
```

### 功能流程

```
上傳文件 → 文本分割 → 向量化 → 存儲 FAISS DB
                              ↓
                          使用者提問
                              ↓
                        檢索相關文件
                              ↓
                    使用 Gemini 生成答案
                              ↓
                         顯示結果
```

## 🚀 快速開始

### 前置條件

1. **Python 3.8+**
2. **Google API Key** (用於 Gemini)
   - 前往: https://aistudio.google.com/app/apikey
   - 建立新的 API Key

3. **HuggingFace Token** (用於 EmbeddingGemma)
   - 前往: https://huggingface.co/settings/tokens
   - 建立新的 Read Token

### 安裝步驟

#### 1. 克隆或下載專案

```bash
cd c:\Users\falle\Desktop\hw4
```

#### 2. 建立虛擬環境（推薦）

```bash
# 使用 Python venv
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

#### 4. 運行 Streamlit 應用

```bash
streamlit run streamlit_app.py
```

應用將在 `http://localhost:8501` 打開

## 📖 使用指南

### 第一步：配置 API

1. 打開側邊欄的「⚙️ 配置」
2. 輸入您的 **HuggingFace Token**
3. 輸入您的 **Google API Key**

### 第二步：建立向量資料庫

#### 選項 A：上傳新文件

1. 切換到「📤 建立資料庫」標籤
2. 選擇「建立新資料庫」模式
3. 上傳一個或多個文件 (.pdf, .txt, .docx)
4. 點擊「🔨 建立向量資料庫」
5. 等待處理完成（可能需要數分鐘）
6. 可選：點擊「💾 保存資料庫」以供後續使用

#### 選項 B：載入已保存的資料庫

1. 切換到「📤 建立資料庫」標籤
2. 選擇「載入現有資料庫」模式
3. 點擊「📂 載入 faiss_db 資料庫」
4. 等待載入完成

### 第三步：提問

1. 切換到「❓ 提問」標籤
2. 在文本區輸入您的問題
3. 點擊「🚀 取得答案」
4. 系統將：
   - 檢索相關文件片段
   - 通過 Gemini 生成答案
   - 顯示最終答案和來源片段

## 🔧 核心模組說明

### 1. `embeddings.py` - 自定義嵌入模型

```python
class EmbeddingGemmaEmbeddings(HuggingFaceEmbeddings)
```

**功能**:
- 使用 Google 的 EmbeddingGemma-300m 模型
- 遵循 Google 推薦的前綴格式：
  - 文件: `title: none | text: {文本}`
  - 查詢: `task: search result | query: {查詢}`

### 2. `rag_chain.py` - RAG 查詢管道

```python
def query_rag(vectorstore, query: str, llm_api_key: str)
```

**流程**:
1. 檢索相關文件 (Top-4)
2. 格式化上下文
3. 構建 LangChain RAG Chain
4. 通過 Gemini 2.5 Flash 生成答案
5. 返回答案和檢索到的文件

### 3. `vector_store.py` - 向量資料庫管理

**主要函數**:

- `create_vector_store(uploaded_files, hf_token)`: 建立新資料庫
  - 載入支持的文件格式
  - 分割文本 (chunk_size=500, overlap=100)
  - 創建 FAISS 向量資料庫

- `save_vectorstore(vectorstore, path)`: 保存資料庫

- `load_vectorstore(path)`: 載入已保存的資料庫

## 📊 文本分割參數

```python
chunk_size=500       # 每個文本塊的大小
chunk_overlap=100    # 塊之間的重疊
```

調整這些參數以改變：
- 檢索的粒度
- 記憶體使用情況
- 查詢效果

## 🌍 多語言支持

系統提示詞已針對**繁體中文**優化：
- 檢索的文件可以是任何語言
- 答案將用繁體中文生成

## 💾 資料庫文件

建立資料庫後，文件將保存在 `faiss_db/` 目錄：

```
faiss_db/
├── index.faiss      # FAISS 向量索引
└── index.pkl        # 文件元數據
```

## ⚠️ 常見問題

### 問題 1: "Import 錯誤"
**解決**: 確保所有依賴已安裝
```bash
pip install -r requirements.txt
```

### 問題 2: "API Key 無效"
**解決**: 
- 確認您使用的是有效的 API Key
- 檢查 API 是否已啟用
- 對於 Google: https://aistudio.google.com/app/apikey
- 對於 HuggingFace: https://huggingface.co/settings/tokens

### 問題 3: "記憶體不足"
**解決**:
- 減少上傳文件大小
- 調整 `chunk_size` 為更小的值
- 使用 GPU 加速（修改 embeddings.py 中的 device）

### 問題 4: "檢索質量不佳"
**解決**:
- 調整 retriever 的 `k` 值 (目前為 4)
- 修改 `chunk_size` 和 `chunk_overlap`
- 確保上傳的文件質量良好

## 🔐 安全建議

1. **不要將 API Key 提交到版本控制**
   - 使用 `.env` 文件（見下方）
   - 添加 `.env` 到 `.gitignore`

2. **使用環境變數**：
   ```bash
   # 在 .env 文件中
   HUGGINGFACE_TOKEN=your_token_here
   GOOGLE_API_KEY=your_key_here
   ```

3. **限制文件大小**
   - 上傳的文件應 < 100MB

## 📈 性能優化

### 向量化優化
```python
# 在 embeddings.py 中修改
embeddings = EmbeddingGemmaEmbeddings(
    model_kwargs={"device": "cuda"},  # 使用 GPU
    show_progress=True
)
```

### 檢索優化
```python
# 在 rag_chain.py 中修改
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # 增加檢索結果
```

## 📚 延伸功能

可以擴展的功能：
- [ ] 支持更多文件格式 (Excel, PowerPoint)
- [ ] 對話記憶 (多轉對話)
- [ ] 文件管理界面
- [ ] 搜索歷史
- [ ] 批量問題處理
- [ ] 自定義 LLM 模型
- [ ] Web 搜索集成

## 🔗 相關資源

- [LangChain 文件](https://python.langchain.com/)
- [Streamlit 文件](https://docs.streamlit.io/)
- [FAISS 文件](https://faiss.ai/)
- [Google Gemini API](https://ai.google.dev/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)

## 📝 代碼示例

### 直接使用 RAG 鏈 (不通過 Streamlit)

```python
from vector_store import load_vectorstore
from rag_chain import query_rag

# 載入向量資料庫
vectorstore = load_vectorstore("faiss_db")

# 執行查詢
query = "這份文件主要講什麼？"
answer, docs = query_rag(vectorstore, query, "your-api-key")

print("答案:", answer)
print("檢索到的文件片段數:", len(docs))
```

### 批量建立多個資料庫

```python
from vector_store import create_vector_store, save_vectorstore

files = ["doc1.pdf", "doc2.docx", "doc3.txt"]

for file in files:
    # 上傳每個文件
    vectorstore = create_vector_store([file], hf_token)
    save_vectorstore(vectorstore, f"db_{file}")
```

## 📄 項目許可

本項目使用以下開源庫：
- LangChain (MIT License)
- Streamlit (Apache License 2.0)
- FAISS (MIT License)
- sentence-transformers (Apache License 2.0)

## 👨‍💻 開發者信息

**建立日期**: 2025-12-01
**版本**: 1.0.0
**主要功能**: 
- RAG 文件問答系統
- Google EmbeddingGemma 集成
- Streamlit Web 界面

## 🤝 貢獻

歡迎提交問題和改進建議！

## ❓ 技術支持

如遇問題，請：
1. 檢查相關日誌
2. 查看常見問題部分
3. 驗證 API Key 有效性
4. 確保所有依賴正確安裝

---

**享受您的 RAG 文件問答系統！** 🚀
