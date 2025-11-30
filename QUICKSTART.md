# 🚀 快速開始指南

## ⏱️ 5 分鐘快速設置

### 前置條件
- Python 3.8 或更高版本
- Google API Key（可選但推薦）
- HuggingFace Token（可選但推薦）

### 安裝步驟

#### 1️⃣ 克隆或下載項目
```bash
cd c:\Users\falle\Desktop\hw4
```

#### 2️⃣ 建立虛擬環境（可選但推薦）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 3️⃣ 安裝依賴
```bash
pip install -r requirements.txt
```

#### 4️⃣ 配置 API 密鑰
```bash
# 複製 .env.example 為 .env
copy .env.example .env

# 編輯 .env 文件，添加你的 API 密鑰
# HUGGINGFACE_TOKEN=your_token
# GOOGLE_API_KEY=your_key
```

#### 5️⃣ 運行應用
```bash
streamlit run streamlit_app.py
```

應用將在 `http://localhost:8501` 打開 ✨

---

## 💡 主要功能概述

### 1. 文件上傳與處理
- 支持 PDF、DOCX、TXT 格式
- 自動文本分割和向量化
- FAISS 向量資料庫創建

### 2. 文件問答
- 檢索相關文件片段
- 使用 Gemini 2.5 Flash 生成答案
- 提供源文件透明度

### 3. 資料庫管理
- 保存和載入向量資料庫
- 多文件支持
- 永久存儲選項

---

## 🔧 核心文件說明

| 文件 | 功能 |
|------|------|
| `streamlit_app.py` | 主應用界面 |
| `embeddings.py` | 自定義嵌入模型 |
| `rag_chain.py` | RAG 查詢管道 |
| `vector_store.py` | 向量資料庫管理 |
| `config.py` | 配置管理 |
| `setup_helper.py` | 設置助手 |
| `test_rag.py` | 測試套件 |

---

## 📝 使用示例

### 基本工作流程

```
1. 啟動應用
   └─> streamlit run streamlit_app.py

2. 配置 API 密鑰
   └─> 在側邊欄輸入 Token

3. 上傳文件
   └─> 選擇一個或多個文件

4. 建立資料庫
   └─> 點擊「建立向量資料庫」

5. 提問
   └─> 在提問標籤輸入問題

6. 獲得答案
   └─> 查看 AI 生成的答案和來源
```

---

## 🐛 故障排除

### 問題：Import 錯誤
```bash
# 解決：重新安裝依賴
pip install -r requirements.txt --upgrade
```

### 問題：API Key 無效
```
1. 驗證 API Key 正確性
2. 檢查是否過期
3. 確認 .env 文件已正確配置
```

### 問題：記憶體不足
```python
# 在 embeddings.py 修改 device：
model_kwargs={"device": "cpu"}  # 改為 "cuda" 使用 GPU
```

### 問題：檢索質量低
```python
# 在 rag_chain.py 調整檢索參數：
retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # 增加 k 值
```

---

## 📚 獲取 API 密鑰

### Google API Key
1. 訪問 https://aistudio.google.com/app/apikey
2. 建立新的 API Key
3. 複製到 `.env` 文件

### HuggingFace Token
1. 訪問 https://huggingface.co/settings/tokens
2. 建立新的 Read Token
3. 複製到 `.env` 文件

---

## 🧪 驗證安裝

運行測試套件驗證一切正常：

```bash
python test_rag.py
```

應該看到所有測試通過 ✅

---

## 📖 完整文檔

詳細文檔請參考 `README.md`

---

## 🎯 下一步

- [ ] 上傳第一份文件
- [ ] 建立向量資料庫
- [ ] 提出第一個問題
- [ ] 探索高級功能
- [ ] 查看 README.md 了解更多

---

## 💬 需要幫助？

1. 檢查 README.md 的常見問題部分
2. 運行 `python test_rag.py` 進行診斷
3. 查看錯誤消息以了解更多信息

---

**祝您使用愉快！🎉**
