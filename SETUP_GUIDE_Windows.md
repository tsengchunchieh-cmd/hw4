# 🚀 RAG 系統 - 使用指南

## ⚠️ 環境說明

您的系統安裝了 **Python 3.13**，而某些依賴包對 Python 3.13 的支持還在進行中。

### 🔧 推薦的解決方案

#### 方案 1：使用 Python 3.10 虛擬環境（推薦）

```powershell
# 1. 下載 Python 3.10（如果未安裝）
# 訪問: https://www.python.org/downloads/

# 2. 創建虛擬環境
py -3.10 -m venv venv310

# 3. 激活虛擬環境
venv310\Scripts\Activate.ps1

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 運行應用
streamlit run streamlit_app.py
```

#### 方案 2：使用 Conda（最簡單）

```powershell
# 1. 安裝 Miniconda
# 訪問: https://docs.conda.io/projects/miniconda/en/latest/

# 2. 創建環境
conda create -n rag python=3.10

# 3. 激活環境
conda activate rag

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 運行應用
streamlit run streamlit_app.py
```

#### 方案 3：Docker（最可靠）

```powershell
# 1. 安裝 Docker Desktop
# 訪問: https://www.docker.com/products/docker-desktop

# 2. 構建鏡像
docker build -t rag-app .

# 3. 運行容器
docker run -p 8501:8501 `
  -e HUGGINGFACE_TOKEN=your_token `
  -e GOOGLE_API_KEY=your_key `
  rag-app
```

---

## 📋 完整安裝步驟

### 步驟 1：檢查 Python 版本

```powershell
# 檢查已安裝的 Python 版本
python --version
py -3.10 --version  # 或其他版本
```

### 步驟 2：創建虛擬環境

```powershell
# 使用 Python 3.10
py -3.10 -m venv venv

# 或使用 Python 3.11
py -3.11 -m venv venv
```

### 步驟 3：激活虛擬環境

```powershell
# Windows PowerShell
venv\Scripts\Activate.ps1

# 如果收到執行策略錯誤，運行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步驟 4：安裝依賴

```powershell
# 升級 pip
python -m pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt

# 或逐個安裝
pip install streamlit langchain langchain-community langchain-google-genai sentence-transformers faiss-cpu pypdf python-docx unstructured
```

### 步驟 5：配置 API 密鑰

```powershell
# 複製範本
copy .env.example .env

# 編輯 .env 並添加你的密鑰：
# HUGGINGFACE_TOKEN=your_token_here
# GOOGLE_API_KEY=your_key_here
```

### 步驟 6：運行應用

```powershell
streamlit run streamlit_app.py
```

應用將在 `http://localhost:8501` 打開

---

## 🆘 故障排除

### 問題 1：pip 錯誤（Python 3.13）

**症狀**: `KeyboardInterrupt` 或 `ImportError`

**解決**:
- 降級到 Python 3.10 或 3.11
- 或使用 Conda 環境
- 或使用 Docker

### 問題 2：虛擬環境激活失敗

**症狀**: `執行策略不允許運行指令檔案`

**解決**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 問題 3：缺少依賴

**症狀**: `ModuleNotFoundError`

**解決**:
```powershell
# 重新安裝依賴
pip install -r requirements.txt --upgrade
```

### 問題 4：Streamlit 無法啟動

**症狀**: 端口 8501 被占用

**解決**:
```powershell
# 使用不同的端口
streamlit run streamlit_app.py --server.port 8502
```

---

## 🐳 使用 Docker（推薦給企業用戶）

### 安裝 Docker

1. 訪問 https://www.docker.com/products/docker-desktop
2. 下載並安裝 Docker Desktop
3. 重啟計算機

### 構建和運行

```powershell
# 構建鏡像（首次）
docker build -t rag-app:latest .

# 運行容器
docker run -it -p 8501:8501 `
  -e HUGGINGFACE_TOKEN="your_token" `
  -e GOOGLE_API_KEY="your_key" `
  rag-app:latest

# 訪問
http://localhost:8501
```

---

## ✅ 驗證安裝

### 運行測試

```powershell
# 激活虛擬環境
venv\Scripts\Activate.ps1

# 運行測試套件
python test_rag.py
```

所有 6 個測試應該通過：
- ✅ 文件結構
- ✅ 配置加載
- ✅ 嵌入模型
- ✅ RAG 管道
- ✅ 向量資料庫
- ✅ API 密鑰

---

## 📚 獲取 API 密鑰

### HuggingFace Token

1. 訪問 https://huggingface.co/settings/tokens
2. 點擊「New token」
3. 選擇「Read」權限
4. 複製 token
5. 粘貼到 `.env` 文件

### Google API Key

1. 訪問 https://aistudio.google.com/app/apikey
2. 點擊「Create API key」
3. 複製 key
4. 粘貼到 `.env` 文件

---

## 🚀 現在運行應用

```powershell
# 1. 激活虛擬環境
venv\Scripts\Activate.ps1

# 2. 運行應用
streamlit run streamlit_app.py

# 3. 在瀏覽器中訪問
# http://localhost:8501
```

---

## 📖 查看文檔

- **START_HERE.md** - 快速概覽
- **QUICKSTART.md** - 5 分鐘開始
- **README.md** - 完整指南
- **ARCHITECTURE.md** - 系統架構
- **DEPLOYMENT.md** - 部署指南
- **INSTALLATION_CHECKLIST.md** - 安裝驗證

---

## 💡 提示

- 使用 Python 3.10 或 3.11 獲得最佳兼容性
- 使用虛擬環境隔離依賴
- 定期更新依賴：`pip install -r requirements.txt --upgrade`
- 保護您的 API 密鑰（不要提交到 Git）

---

**祝您使用愉快！** 🎉

有任何問題，請參考完整文檔或檢查 README.md 的常見問題部分。
