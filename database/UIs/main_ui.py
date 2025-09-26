# python -m streamlit run database/UIs/main_ui.py

import streamlit as st

def main():
    st.set_page_config(
        page_title="Transcript & Embedding Tools",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Transcript & Embedding Tools")
    st.markdown("Choose from the available tools below:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📝 YouTube Transcript Extractor")
        st.markdown("Extract transcripts from YouTube videos easily!")
        st.markdown("**Features:**")
        st.markdown("• Extract transcripts from any YouTube video")
        st.markdown("• Download transcripts as text files")
        st.markdown("• Support for various YouTube URL formats")
        
        if st.button("Launch YouTube Extractor", type="primary", use_container_width=True):
            st.info("To run the YouTube Transcript Extractor, use:")
            st.code("python -m streamlit run database/UIs/streamlit_app.py")
    
    with col2:
        st.header("🧠 Embedding Utility Interface")
        st.markdown("Generate embeddings, manage vector databases, and perform semantic search!")
        st.markdown("**Features:**")
        st.markdown("• Generate text embeddings using OpenAI")
        st.markdown("• Store and query vectors in Pinecone")
        st.markdown("• Batch processing and semantic search")
        st.markdown("• Interactive vector management")
        
        if st.button("Launch Embedding Utility", type="primary", use_container_width=True):
            st.info("To run the Embedding Utility Interface, use:")
            st.code("python -m streamlit run database/UIs/embedding_ui.py")
    
    st.markdown("---")
    
    # Quick start instructions
    st.header("🚀 Quick Start")
    st.markdown("""
    ### Prerequisites
    1. **Install dependencies:**
       ```bash
       pip install -r req.txt
       ```
    
    2. **Set up environment variables:**
       Create a `.env` file in the project root with:
       ```
       OPENAI_API_KEY=your_openai_api_key_here
       PINECONE_API_KEY=your_pinecone_api_key_here
       ```
    
    ### Running the Applications
    - **YouTube Transcript Extractor:** `python -m streamlit run database/UIs/streamlit_app.py`
    - **Embedding Utility:** `python -m streamlit run database/UIs/embedding_ui.py`
    - **This launcher:** `python -m streamlit run database/UIs/main_ui.py`
    
    ### Features Overview
    - **YouTube Transcript Extractor:** Simple interface for extracting video transcripts
    - **Embedding Utility:** Advanced interface for text embeddings and vector operations
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
