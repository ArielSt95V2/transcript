# python -m streamlit run database/UIs/embedding_ui.py

import streamlit as st
import os
import json
from typing import List, Dict, Any
import pandas as pd
from database.utils.embed import EmbeddingUtility

def main():
    st.set_page_config(
        page_title="Embedding Utility Interface",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Embedding Utility Interface")
    st.markdown("Generate embeddings, manage vector databases, and perform semantic search using OpenAI and Pinecone.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys
        st.subheader("API Keys")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key"
        )
        
        pinecone_key = st.text_input(
            "Pinecone API Key", 
            type="password",
            value=os.getenv("PINECONE_API_KEY", ""),
            help="Enter your Pinecone API key"
        )
        
        # Model Configuration
        st.subheader("Model Settings")
        embedding_model = st.selectbox(
            "Embedding Model",
            ["text-embedding-3-large", "text-embedding-3-small", "text-embedding-ada-002"],
            index=0
        )
        
        index_name = st.text_input(
            "Pinecone Index Name",
            value="learning-assistant",
            help="Name of the Pinecone index to use"
        )
        
        dimension = st.number_input(
            "Vector Dimension",
            value=3072,
            min_value=1,
            max_value=8192,
            help="Dimension of the embedding vectors"
        )
    
    # Initialize EmbeddingUtility
    if openai_key and pinecone_key:
        try:
            embedding_util = EmbeddingUtility(
                openai_api_key=openai_key,
                pinecone_api_key=pinecone_key,
                embedding_model=embedding_model,
                index_name=index_name,
                dimension=dimension
            )
            st.success("✅ EmbeddingUtility initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize EmbeddingUtility: {str(e)}")
            embedding_util = None
    else:
        st.warning("⚠️ Please provide both OpenAI and Pinecone API keys to use the embedding functionality.")
        embedding_util = None
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Text Embedding", 
        "📊 Batch Processing", 
        "🔍 Vector Search", 
        "🗄️ Vector Management", 
        "📈 Analytics"
    ])
    
    with tab1:
        st.header("📝 Single Text Embedding")
        
        if embedding_util:
            text_input = st.text_area(
                "Enter text to embed:",
                placeholder="Type your text here...",
                height=100
            )
            
            if st.button("Generate Embedding", type="primary"):
                if text_input.strip():
                    with st.spinner("Generating embedding..."):
                        try:
                            embedding = embedding_util.embed_single_text(text_input)
                            st.success("✅ Embedding generated successfully!")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("Embedding Vector")
                                st.text(f"Dimension: {len(embedding)}")
                                st.text(f"First 10 values: {embedding[:10]}")
                                
                            with col2:
                                st.subheader("Vector Statistics")
                                import numpy as np
                                embedding_array = np.array(embedding)
                                st.metric("Mean", f"{embedding_array.mean():.6f}")
                                st.metric("Std Dev", f"{embedding_array.std():.6f}")
                                st.metric("Min", f"{embedding_array.min():.6f}")
                                st.metric("Max", f"{embedding_array.max():.6f}")
                        except Exception as e:
                            st.error(f"❌ Error generating embedding: {str(e)}")
                else:
                    st.warning("⚠️ Please enter some text to embed.")
        else:
            st.info("Please configure API keys in the sidebar to use this feature.")
    
    with tab2:
        st.header("📊 Batch Text Processing")
        
        if embedding_util:
            # Input method selection
            input_method = st.radio(
                "Choose input method:",
                ["Manual Entry", "File Upload", "JSON Input"]
            )
            
            data = []
            
            if input_method == "Manual Entry":
                st.subheader("Manual Data Entry")
                num_items = st.number_input("Number of items", min_value=1, max_value=100, value=3)
                
                for i in range(num_items):
                    with st.expander(f"Item {i+1}"):
                        item_id = st.text_input(f"ID {i+1}", value=f"item_{i+1}")
                        item_text = st.text_area(f"Text {i+1}", placeholder="Enter text here...")
                        if item_id and item_text:
                            data.append({"id": item_id, "text": item_text})
            
            elif input_method == "File Upload":
                st.subheader("File Upload")
                uploaded_file = st.file_uploader("Upload a text file", type=['txt', 'csv', 'json'])
                
                if uploaded_file:
                    if uploaded_file.type == "text/plain":
                        content = uploaded_file.read().decode("utf-8")
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.strip():
                                data.append({"id": f"line_{i+1}", "text": line.strip()})
                    elif uploaded_file.type == "text/csv":
                        df = pd.read_csv(uploaded_file)
                        for _, row in df.iterrows():
                            data.append({"id": str(row.iloc[0]), "text": str(row.iloc[1])})
                    elif uploaded_file.type == "application/json":
                        json_data = json.loads(uploaded_file.read())
                        data = json_data if isinstance(json_data, list) else [json_data]
            
            elif input_method == "JSON Input":
                st.subheader("JSON Input")
                json_input = st.text_area("Enter JSON data:", height=200)
                if json_input:
                    try:
                        data = json.loads(json_input)
                        if not isinstance(data, list):
                            data = [data]
                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON format")
                        data = []
            
            # Process data
            if data and st.button("Process and Store Vectors", type="primary"):
                with st.spinner("Processing data..."):
                    try:
                        success = embedding_util.batch_process_and_store(data)
                        if success:
                            st.success(f"✅ Successfully processed and stored {len(data)} vectors!")
                        else:
                            st.error("❌ Failed to process and store vectors")
                    except Exception as e:
                        st.error(f"❌ Error processing data: {str(e)}")
            
            # Display data preview
            if data:
                st.subheader("Data Preview")
                st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("Please configure API keys in the sidebar to use this feature.")
    
    with tab3:
        st.header("🔍 Vector Search")
        
        if embedding_util:
            query_text = st.text_area(
                "Enter search query:",
                placeholder="What are you looking for?",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                top_k = st.number_input("Number of results", min_value=1, max_value=20, value=5)
            with col2:
                namespace = st.text_input("Namespace", value="default")
            
            if st.button("Search Vectors", type="primary"):
                if query_text.strip():
                    with st.spinner("Searching vectors..."):
                        try:
                            results = embedding_util.query_vectors(
                                query_text, 
                                top_k=top_k, 
                                namespace=namespace
                            )
                            
                            st.success(f"✅ Found {len(results.matches)} results!")
                            
                            for i, match in enumerate(results.matches):
                                with st.expander(f"Result {i+1} (Score: {match.score:.3f})"):
                                    if hasattr(match, 'metadata') and match.metadata:
                                        for key, value in match.metadata.items():
                                            if key == 'text':
                                                st.text_area(f"{key.title()}:", value=str(value), height=100)
                                            else:
                                                st.text(f"{key.title()}: {value}")
                                    else:
                                        st.text(f"ID: {match.id}")
                        except Exception as e:
                            st.error(f"❌ Error searching vectors: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a search query.")
        else:
            st.info("Please configure API keys in the sidebar to use this feature.")
    
    with tab4:
        st.header("🗄️ Vector Management")
        
        if embedding_util:
            st.subheader("Index Information")
            
            if st.button("Get Index Stats", type="primary"):
                try:
                    # This would require additional methods in the EmbeddingUtility class
                    st.info("Index stats functionality would require additional implementation")
                except Exception as e:
                    st.error(f"❌ Error getting index stats: {str(e)}")
            
            st.subheader("Available Models")
            if st.button("Get Available Models"):
                try:
                    models = embedding_util.get_available_models()
                    if models:
                        st.success(f"✅ Found {len(models)} available models:")
                        for model in models:
                            st.text(f"• {model}")
                    else:
                        st.info("No models found or error retrieving models")
                except Exception as e:
                    st.error(f"❌ Error getting models: {str(e)}")
        else:
            st.info("Please configure API keys in the sidebar to use this feature.")
    
    with tab5:
        st.header("📈 Analytics & Testing")
        
        if embedding_util:
            st.subheader("Example Usage")
            
            if st.button("Run Example", type="primary"):
                with st.spinner("Running example..."):
                    try:
                        # Sample data for demonstration
                        sample_data = [
                            {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
                            {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
                            {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
                            {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
                            {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
                        ]
                        
                        # Process and store
                        success = embedding_util.batch_process_and_store(sample_data, namespace="demo")
                        if success:
                            st.success("✅ Sample data processed and stored!")
                            
                            # Query example
                            query = "Tell me about the tech company known as Apple"
                            results = embedding_util.query_vectors(query, top_k=3, namespace="demo")
                            
                            st.subheader("Query Results")
                            st.text(f"Query: {query}")
                            
                            for i, match in enumerate(results.matches):
                                st.text(f"{i+1}. {match.metadata['text']} (Score: {match.score:.3f})")
                        else:
                            st.error("❌ Failed to process sample data")
                    except Exception as e:
                        st.error(f"❌ Error running example: {str(e)}")
            
            st.subheader("Performance Metrics")
            st.info("Performance metrics would be displayed here after operations are performed.")
        else:
            st.info("Please configure API keys in the sidebar to use this feature.")
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and the EmbeddingUtility class")

if __name__ == "__main__":
    main()
