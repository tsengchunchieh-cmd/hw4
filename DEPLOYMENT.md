# 🌐 部署指南

本文檔提供在不同環境部署 RAG 應用的完整說明。

---

## 📋 部署選項對比

| 方式 | 難度 | 成本 | 易用性 | 推薦用途 |
|-----|------|------|--------|---------|
| 本地運行 | ⭐ | 免費 | ⭐⭐⭐⭐⭐ | 開發、測試 |
| Streamlit Cloud | ⭐⭐ | 免費/付費 | ⭐⭐⭐⭐ | 演示、內部使用 |
| Docker | ⭐⭐⭐ | 低 | ⭐⭐⭐ | 生產環境 |
| 雲端 (AWS/GCP) | ⭐⭐⭐⭐ | 中等 | ⭐⭐⭐ | 企業級應用 |

---

## 🏠 本地部署

### 最簡單的方式

```bash
# 1. 進入項目目錄
cd c:\Users\falle\Desktop\hw4

# 2. 創建虛擬環境
python -m venv venv
venv\Scripts\activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 配置 API 密鑰
copy .env.example .env
# 編輯 .env 添加你的 API 密鑰

# 5. 運行應用
streamlit run streamlit_app.py
```

### 訪問應用
```
http://localhost:8501
```

---

## ☁️ Streamlit Cloud 部署

### 前置條件
- GitHub 帳戶
- Streamlit Cloud 帳戶

### 部署步驟

#### 1. 準備 GitHub 倉庫

```bash
# 初始化 Git 倉庫
git init
git add .
git commit -m "Initial RAG application commit"

# 創建 GitHub 倉庫並推送
# (按照 GitHub 的指示)
git remote add origin https://github.com/your-username/rag-app.git
git branch -M main
git push -u origin main
```

#### 2. 確保 requirements.txt 存在

```bash
# 已經包含在項目中
requirements.txt
```

#### 3. 在 Streamlit Cloud 部署

1. 訪問 https://streamlit.io/cloud
2. 點擊「New app」
3. 連接你的 GitHub 倉庫
4. 選擇分支和文件: `streamlit_app.py`
5. 點擊「Deploy」

#### 4. 配置 Secrets

在 Streamlit Cloud 中配置 API 密鑰：

1. 進入應用設置
2. 點擊「Secrets」
3. 添加以下內容：

```ini
HUGGINGFACE_TOKEN = "your_token_here"
GOOGLE_API_KEY = "your_key_here"
```

#### 5. 公開應用 URL

應用將自動部署到 URL，如：
```
https://your-app-name.streamlit.app
```

---

## 🐳 Docker 部署

### 1. 創建 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit 配置
RUN mkdir -p ~/.streamlit

RUN echo "\
[server]\n\
headless = true\n\
port = 8501\n\
enableXsrfProtection = false\n\
" > ~/.streamlit/config.toml

# 暴露端口
EXPOSE 8501

# 運行應用
CMD ["streamlit", "run", "streamlit_app.py"]
```

### 2. 創建 .dockerignore

```
.git
.gitignore
__pycache__
*.pyc
*.pyo
.venv
venv/
.env
.env.local
faiss_db/
uploaded_docs/
logs/
.DS_Store
Thumbs.db
```

### 3. 構建和運行 Docker 鏡像

```bash
# 構建鏡像
docker build -t rag-app:latest .

# 運行容器
docker run -p 8501:8501 \
  -e HUGGINGFACE_TOKEN="your_token" \
  -e GOOGLE_API_KEY="your_key" \
  -e STREAMLIT_SERVER_HEADLESS=true \
  rag-app:latest

# 或使用 .env 文件
docker run -p 8501:8501 \
  --env-file .env \
  -e STREAMLIT_SERVER_HEADLESS=true \
  rag-app:latest
```

### 4. 訪問應用
```
http://localhost:8501
```

---

## 🚀 Google Cloud Run 部署

### 前置條件
- Google Cloud 帳戶
- Google Cloud CLI 已安裝

### 部署步驟

#### 1. 認證

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### 2. 創建 cloudbuild.yaml

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/rag-app:latest'
      - '.'
  
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/rag-app:latest'
  
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - 'run'
      - '--filename=k8s/'
      - '--image=gcr.io/$PROJECT_ID/rag-app:latest'
      - '--location=us-central1'
      - '--cluster=rag-cluster'
```

#### 3. 部署

```bash
# 使用 Cloud Run
gcloud run deploy rag-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars HUGGINGFACE_TOKEN=your_token,GOOGLE_API_KEY=your_key
```

---

## 🏢 AWS Lambda 部署

### 使用 AWS Serverless Application Model (SAM)

#### 1. 安裝 SAM CLI

```bash
# Windows
choco install aws-sam-cli

# macOS
brew tap aws/tap
brew install aws-sam-cli

# Linux
pip install aws-sam-cli
```

#### 2. 創建 template.yaml

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  RAGFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: python3.10
      Timeout: 300
      MemorySize: 3008
      Environment:
        Variables:
          HUGGINGFACE_TOKEN: !Ref HFToken
          GOOGLE_API_KEY: !Ref GoogleKey
      Events:
        Api:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY

Parameters:
  HFToken:
    Type: String
    NoEcho: true
  GoogleKey:
    Type: String
    NoEcho: true
```

#### 3. 部署

```bash
sam build
sam deploy --guided
```

---

## 🔧 環境變數配置

### 本地

```bash
# .env
HUGGINGFACE_TOKEN=your_token
GOOGLE_API_KEY=your_key
```

### Docker

```bash
# 使用環境變數
docker run -e HUGGINGFACE_TOKEN=... -e GOOGLE_API_KEY=... rag-app

# 使用 .env 文件
docker run --env-file .env rag-app
```

### Streamlit Cloud

```
Secrets (在應用設置中)：
HUGGINGFACE_TOKEN
GOOGLE_API_KEY
```

### 雲端平台

```bash
# Google Cloud Run
gcloud run deploy --set-env-vars KEY=value

# AWS Lambda
sam deploy --parameter-overrides HFToken=... GoogleKey=...
```

---

## 📊 性能優化

### 本地

```python
# 在 embeddings.py 使用 GPU
embeddings = EmbeddingGemmaEmbeddings(
    model_kwargs={"device": "cuda"},
    show_progress=True
)
```

### Docker

```dockerfile
# 使用 NVIDIA GPU
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# 安裝 Python 和依賴
# ...
```

### 雲端

```bash
# Google Cloud Run with GPU
gcloud run deploy rag-app \
  --gpu=1 \
  --memory=8Gi
```

---

## 🔐 安全部署

### 前置條件檢查

```bash
# 確保沒有 .env 文件被提交
git log --all --full-history -- .env

# 確保 secrets 不在代碼中
grep -r "HUGGINGFACE_TOKEN" --include="*.py"
grep -r "GOOGLE_API_KEY" --include="*.py"
```

### 使用密鑰管理

```bash
# Google Cloud Secret Manager
gcloud secrets create huggingface-token --data-file=-
gcloud secrets create google-api-key --data-file=-

# AWS Secrets Manager
aws secretsmanager create-secret \
  --name rag/huggingface-token \
  --secret-string "..."
```

### 認證和授權

```python
# 在 Streamlit 中添加認證
import streamlit as st

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# 簡單的密碼保護
password = st.text_input("Password", type="password")
if password == st.secrets.get("APP_PASSWORD"):
    st.session_state['authenticated'] = True

if st.session_state['authenticated']:
    # 顯示應用
    pass
```

---

## 📈 監控和日誌

### 本地

```bash
# 查看 Streamlit 日誌
streamlit run streamlit_app.py --logger.level=debug
```

### Docker

```bash
# 查看容器日誌
docker logs -f container_id

# 使用 Docker Compose 和 ELK Stack
# (見 docker-compose.yml)
```

### 雲端

```bash
# Google Cloud Logging
gcloud logging read "resource.type=cloud_run_revision"

# AWS CloudWatch
aws logs tail /aws/lambda/rag-app --follow
```

---

## 🔄 CI/CD 設置

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Streamlit Cloud
        run: |
          pip install streamlit
          streamlit run streamlit_app.py
```

---

## 🚨 故障排除

### Docker 問題

```bash
# 查看構建日誌
docker build --progress=plain .

# 進入容器調試
docker exec -it container_id /bin/bash

# 檢查網絡連接
docker network ls
docker inspect network_name
```

### 性能問題

```python
# 減少 chunk_size
CHUNK_SIZE = 250  # 默認 500

# 減少 retriever k 值
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 使用緩存
@st.cache_resource
def load_vectorstore():
    return load_vectorstore("faiss_db")
```

### 記憶體問題

```bash
# Docker 內存限制
docker run -m 8g rag-app

# 使用更輕量的模型
# 見 config.py
```

---

## 📚 相關資源

- [Streamlit Cloud 文檔](https://docs.streamlit.io/streamlit-cloud)
- [Docker 文檔](https://docs.docker.com/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)

---

**祝部署順利！🚀**
