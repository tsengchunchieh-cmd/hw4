# ✅ 安裝驗證清單

使用本清單確保您的 RAG 應用已正確安裝和配置。

---

## 📋 安裝前檢查

- [ ] Python 3.8+ 已安裝
  ```bash
  python --version
  ```

- [ ] pip 已安裝
  ```bash
  pip --version
  ```

- [ ] 有效的網絡連接（用於下載模型和 API 調用）

- [ ] 充足的磁盤空間（至少 5GB）
  - 虛擬環境: ~1.5GB
  - 模型: ~2GB
  - 資料庫: 變量

---

## 🔑 API 密鑰準備

### HuggingFace Token
- [ ] 訪問 https://huggingface.co/settings/tokens
- [ ] 建立新的 Read Token
- [ ] 複製 Token 值
- [ ] 妥善保管（勿分享）

### Google API Key
- [ ] 訪問 https://aistudio.google.com/app/apikey
- [ ] 建立新的 API Key
- [ ] 複製 Key 值
- [ ] 確保 Gemini API 已啟用
- [ ] 妥善保管（勿分享）

---

## 📦 安裝步驟驗證

### 1. 創建虛擬環境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

- [ ] 虛擬環境已創建
- [ ] 虛擬環境已啟動（提示符前有 `(venv)` ）

### 2. 升級 pip
```bash
pip install --upgrade pip
```

- [ ] pip 已升級到最新版本

### 3. 安裝依賴
```bash
pip install -r requirements.txt
```

- [ ] 所有依賴已成功安裝
- [ ] 無錯誤或警告

### 4. 驗證安裝
```bash
python test_rag.py
```

- [ ] 所有 6 個測試通過
- [ ] 沒有紅色的 ❌ 標記

---

## 🔧 配置驗證

### 1. 環境文件設置
```bash
# 複製模板
copy .env.example .env
```

- [ ] `.env` 文件已創建

### 2. 編輯配置
```
使用文本編輯器打開 .env：
1. 設置 HUGGINGFACE_TOKEN
2. 設置 GOOGLE_API_KEY
3. 保存文件
```

- [ ] `HUGGINGFACE_TOKEN` 已設置
- [ ] `GOOGLE_API_KEY` 已設置
- [ ] 文件已保存

### 3. 驗證配置
```bash
python -c "from config import validate_api_keys; print(validate_api_keys())"
```

- [ ] 返回 `(True, [])`（已配置所有密鑰）

---

## 📁 文件結構驗證

檢查以下文件是否存在：

### 核心文件
- [ ] `streamlit_app.py` (主應用)
- [ ] `embeddings.py` (向量模型)
- [ ] `rag_chain.py` (RAG 管道)
- [ ] `vector_store.py` (資料庫管理)
- [ ] `config.py` (配置管理)

### 工具文件
- [ ] `setup_helper.py` (設置助手)
- [ ] `test_rag.py` (測試套件)

### 配置文件
- [ ] `requirements.txt` (依賴列表)
- [ ] `.env` (環境配置)
- [ ] `.env.example` (配置模板)
- [ ] `.gitignore` (Git 忽略規則)

### 文檔文件
- [ ] `README.md` (完整指南)
- [ ] `QUICKSTART.md` (快速開始)
- [ ] `ARCHITECTURE.md` (系統架構)
- [ ] `DEPLOYMENT.md` (部署指南)
- [ ] `PROJECT_SUMMARY.md` (項目總結)
- [ ] `INSTALLATION_CHECKLIST.md` (此文件)

---

## 🧪 功能驗證

### 1. 模塊導入
```bash
python -c "from embeddings import EmbeddingGemmaEmbeddings; print('✓ embeddings')"
python -c "from rag_chain import query_rag; print('✓ rag_chain')"
python -c "from vector_store import create_vector_store; print('✓ vector_store')"
python -c "from config import validate_api_keys; print('✓ config')"
```

- [ ] 所有模塊導入成功

### 2. 配置驗證
```bash
python -c "from config import get_config_summary; import json; print(json.dumps(get_config_summary(), indent=2))"
```

- [ ] 配置已成功加載
- [ ] 顯示模型名稱、參數等信息

### 3. 向量化測試
```python
from embeddings import EmbeddingGemmaEmbeddings

embeddings = EmbeddingGemmaEmbeddings()
# 應該成功初始化（第一次會下載模型）
```

- [ ] 模型已下載（首次需要時間）
- [ ] 向量化類已初始化

### 4. 應用啟動
```bash
streamlit run streamlit_app.py
```

- [ ] Streamlit 應用已啟動
- [ ] 瀏覽器自動打開 `http://localhost:8501`
- [ ] UI 正確顯示

---

## 🚀 首次運行驗證

### 1. 側邊欄配置
- [ ] 能夠輸入 HuggingFace Token
- [ ] 能夠輸入 Google API Key
- [ ] 配置已正確保存

### 2. 文件上傳
- [ ] 文件上傳控件可見
- [ ] 能夠選擇 PDF/DOCX/TXT 文件
- [ ] 支持多文件選擇

### 3. 資料庫建立
- [ ] 「建立向量資料庫」按鈕可用
- [ ] 點擊後顯示進度提示
- [ ] 完成後顯示成功消息

### 4. 提問功能
- [ ] 能夠輸入問題
- [ ] 「取得答案」按鈕可用
- [ ] 顯示 AI 回答
- [ ] 顯示來源文件片段

---

## 🔍 常見問題解決

### 問題：`ModuleNotFoundError`
```
解決步驟：
1. 確認虛擬環境已啟動
2. 運行 pip install -r requirements.txt
3. 檢查是否有錯誤消息
```

- [ ] 已確認虛擬環境
- [ ] 已重新安裝依賴
- [ ] 導入錯誤已解決

### 問題：API Key 無效
```
解決步驟：
1. 驗證 API Key 正確無誤
2. 檢查 API 是否已啟用
3. 確認 .env 格式正確
```

- [ ] 已驗證 API Key
- [ ] API 已啟用
- [ ] .env 格式正確

### 問題：記憶體不足
```
解決步驟：
1. 使用 GPU（如果可用）
2. 減少 chunk_size
3. 使用較小的文件
```

- [ ] 已調整內存設置
- [ ] 已優化參數

### 問題：網絡連接
```
解決步驟：
1. 檢查互聯網連接
2. 檢查防火牆設置
3. 驗證 API 端點可訪問
```

- [ ] 網絡連接正常
- [ ] 防火牆已配置

---

## ✨ 優化檢查

### 性能優化
- [ ] 考慮使用 GPU（修改 device 設置）
- [ ] 根據需要調整 chunk_size
- [ ] 根據需要調整 retriever k 值

### 安全優化
- [ ] `.env` 文件未提交到版本控制
- [ ] API Key 未暴露在代碼中
- [ ] 敏感文件在 `.gitignore` 中

### 代碼質量
- [ ] 無未使用的導入
- [ ] 無明顯的代碼異味
- [ ] 代碼格式一致

---

## 📊 安裝完成度

| 項目 | 狀態 | 備註 |
|------|------|------|
| Python 環境 | ✅/❌ | |
| 依賴安裝 | ✅/❌ | |
| API 配置 | ✅/❌ | |
| 文件結構 | ✅/❌ | |
| 功能測試 | ✅/❌ | |
| 應用啟動 | ✅/❌ | |

---

## 🎯 後續步驟

完成上述所有檢查後：

1. **創建您的第一個資料庫**
   - 上傳測試文件
   - 建立向量資料庫
   - 測試提問功能

2. **探索高級功能**
   - 保存和載入資料庫
   - 調整參數
   - 查看效果

3. **部署應用**（可選）
   - 選擇部署方式（本地/雲端）
   - 按照 DEPLOYMENT.md 部署
   - 分享給他人使用

4. **自定義和改進**
   - 調整提示詞
   - 優化參數
   - 添加新功能

---

## 📞 如需幫助

- 📖 查看 `README.md` - 完整指南和 FAQ
- ⚡ 查看 `QUICKSTART.md` - 快速開始
- 🏗️ 查看 `ARCHITECTURE.md` - 系統設計
- 🚀 查看 `DEPLOYMENT.md` - 部署指南
- 📋 查看 `PROJECT_SUMMARY.md` - 項目總結

---

## ✅ 最終確認

- [ ] 所有檢查項已完成
- [ ] 沒有任何 ❌ 標記
- [ ] 應用已成功啟動
- [ ] 已進行基本功能測試

**祝賀！您的 RAG 系統已準備好使用！** 🎉

---

**日期**: ________________  
**檢查者**: ________________  
**狀態**: ✅ 已驗證 / ⏳ 進行中 / ❌ 需要修復

---

**提示**: 完成此清單後，您可以：
1. 保存此文件以備將來參考
2. 開始使用應用
3. 查看其他文檔了解更多信息
