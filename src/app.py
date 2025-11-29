"""
Streamlit Web Application
User-friendly web interface for the Company Knowledge Base Chatbot.
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from chatbot import CompanyKBChatbot

# Page configuration
st.set_page_config(
    page_title="Company Knowledge Base",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    with st.spinner("🔄 Initializing chatbot..."):
        try:
            st.session_state.chatbot = CompanyKBChatbot(model="llama2")
            st.session_state.initialized = True
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {e}")
            st.stop()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown('<h1 class="main-header">📚 Company Knowledge Base Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask me anything about company policies, benefits, and procedures!</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This AI-powered chatbot helps you find information from company documents using:
    
    - 🧠 **RAG (Retrieval Augmented Generation)**
    - 🤖 **Ollama (Local LLM)**
    - 📊 **ChromaDB (Vector Database)**
    - 🔍 **Semantic Search**
    
    All responses are based on official company documents.
    """)
    
    st.divider()
    
    st.header("💡 Sample Questions")
    sample_questions = [
        "How many vacation days do I get?",
        "What is the remote work policy?",
        "How do I submit expenses?",
        "What are the paid holidays?",
        "Can contractors work remotely?",
    ]
    
    for question in sample_questions:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.sample_question = question
    
    st.divider()
    
    # Knowledge base stats
    st.header("📊 Knowledge Base")
    if st.session_state.initialized:
        doc_count = st.session_state.chatbot.vector_store.get_count()
        st.metric("Indexed Documents", doc_count)
        st.caption("Last updated: Today")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chatbot.clear_history()
        st.rerun()

# Main chat interface
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📎 View Sources"):
                for source in message["sources"]:
                    st.caption(f"• {source}")

# Handle sample question from sidebar
if 'sample_question' in st.session_state:
    user_input = st.session_state.sample_question
    del st.session_state.sample_question
else:
    user_input = None

# Chat input
if prompt := (user_input or st.chat_input("Ask a question about company policies...")):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.chatbot.chat(prompt)
                
                # Display answer
                st.markdown(response["answer"])
                
                # Display sources
                if response["sources"]:
                    with st.expander("📎 View Sources"):
                        for source in response["sources"]:
                            st.caption(f"• {source}")
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response["sources"]
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })

# Footer
st.divider()
st.caption("💡 Tip: Responses may take 1-2 minutes to generate as the AI processes your question locally.")
st.caption("⚠️ This chatbot provides information based on company documents. For official guidance, please contact HR.")