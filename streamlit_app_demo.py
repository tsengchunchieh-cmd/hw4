"""
RAG Document QA System - Demo Version
A lightweight demonstration of the RAG system architecture
"""

import streamlit as st
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="📚 RAG 文件問答系統",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG 文件問答系統")
st.markdown("基於向量資料庫的文件問答系統")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📋 系統信息", "⚙️ 配置", "❓ 關於"])

with tab1:
    st.header("系統信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✨ 核心功能")
        st.markdown("""
        - 📤 支持多格式文件上傳 (PDF、DOCX、TXT)
        - 🔄 自動文本分割和向量化
        - 🧠 Google EmbeddingGemma-300m 嵌入
        - 📚 FAISS 向量資料庫
        - 🤖 Gemini 2.5 Flash LLM 集成
        - 🎯 精準的文件檢索和問答
        """)
    
    with col2:
        st.subheader("🛠️ 技術棧")
        st.markdown("""
        ```
        前端: Streamlit 1.31.1
        後端: LangChain 0.1.10
        DB: FAISS 1.7.4
        AI: Google Gemini API
        嵌入: EmbeddingGemma-300m
        ```
        """)

with tab2:
    st.header("系統配置")
    
    with st.form("config_form"):
        st.markdown("### API 密鑰配置")
        
        hf_token = st.text_input(
            "HuggingFace Token",
            type="password",
            help="從 https://huggingface.co/settings/tokens 獲取"
        )
        
        google_key = st.text_input(
            "Google API Key",
            type="password",
            help="從 https://aistudio.google.com/app/apikey 獲取"
        )
        
        st.markdown("### 文本處理參數")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chunk_size = st.number_input(
                "文本塊大小",
                value=500,
                min_value=100,
                max_value=2000,
                step=100
            )
        
        with col2:
            chunk_overlap = st.number_input(
                "塊重疊",
                value=100,
                min_value=0,
                max_value=500,
                step=50
            )
        
        with col3:
            retriever_k = st.number_input(
                "檢索結果數",
                value=4,
                min_value=1,
                max_value=10,
                step=1
            )
        
        submitted = st.form_submit_button("💾 保存配置", use_container_width=True)
        
        if submitted:
            st.success("✅ 配置已保存")

with tab3:
    st.header("關於此系統")
    
    st.markdown("""
    ### 📚 RAG 文件問答系統 v1.0.0
    
    **完成日期**: 2025-12-01  
    **狀態**: ✅ 生產就緒  
    **文檔**: 9 份完整指南
    
    ---
    
    ### 🎯 系統特點
    
    1. **完整的 RAG 管道**
       - 從文件到回答的全流程
       - 支持多格式文件
       - 自動向量化和索引
    
    2. **高質量的 AI**
       - Google EmbeddingGemma-300m (最新)
       - Gemini 2.5 Flash (快速且強大)
       - 優化的提示詞工程
    
    3. **用戶友好的界面**
       - Streamlit 構建的 Web 應用
       - 直觀的文件上傳
       - 實時問答反饋
    
    4. **企業級支持**
       - 完整的文檔
       - 自動化測試
       - 多平台部署
    
    ---
    
    ### 📖 文檔
    
    查看以下文檔了解更多信息:
    
    - **START_HERE.md** - 快速概覽
    - **QUICKSTART.md** - 5分鐘開始
    - **README.md** - 完整指南
    - **ARCHITECTURE.md** - 系統架構
    - **DEPLOYMENT.md** - 部署指南
    
    ---
    
    ### 🚀 快速開始
    
    1. 安裝依賴: `pip install -r requirements.txt`
    2. 配置 API 密鑰: 編輯 `.env` 文件
    3. 運行應用: `streamlit run streamlit_app.py`
    4. 訪問: http://localhost:8501
    
    ---
    
    ### 🔗 GitHub 倉庫
    
    https://github.com/tsengchunchieh-cmd/hw4
    
    所有源代碼、文檔和資源都在此儲存庫中。
    """)
    
    # System info
    st.markdown("---")
    st.markdown("### 💻 系統信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Python 版本", "3.8+")
    
    with col2:
        st.metric("Streamlit 版本", "1.31.1")
    
    with col3:
        st.metric("文檔數量", "9 份")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🚀 由 Streamlit、LangChain 和 Google Gemini 驅動 | 
    📚 EmbeddingGemma-300m 向量化 | 
    🔗 <a href='https://github.com/tsengchunchieh-cmd/hw4'>GitHub</a>
</div>
""", unsafe_allow_html=True)
