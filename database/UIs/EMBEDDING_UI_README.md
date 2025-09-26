# Embedding Utility Streamlit UI

A comprehensive Streamlit interface for the `EmbeddingUtility` class that provides an easy-to-use web interface for text embedding operations, vector database management, and semantic search.

## Features

### 🧠 Core Functionality
- **Text Embedding**: Generate embeddings for single texts or batch processing
- **Vector Storage**: Store vectors in Pinecone vector database
- **Semantic Search**: Query vectors for similar content
- **Batch Processing**: Process multiple texts at once
- **Vector Management**: Manage and analyze stored vectors

### 🎨 User Interface
- **Interactive Tabs**: Organized interface with separate tabs for different functions
- **Real-time Configuration**: Configure API keys and model settings in the sidebar
- **Data Visualization**: Display embeddings, search results, and statistics
- **Multiple Input Methods**: Manual entry, file upload, or JSON input
- **Progress Indicators**: Visual feedback for long-running operations

## Usage

### Prerequisites
1. Install required dependencies:
   ```bash
   pip install -r req.txt
   ```

2. Set up environment variables in `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

### Running the Application
```bash
python -m streamlit run database/UIs/embedding_ui.py
```

### Interface Overview

#### 📝 Text Embedding Tab
- Generate embeddings for single text inputs
- View embedding vectors and statistics
- Real-time embedding generation

#### 📊 Batch Processing Tab
- Process multiple texts at once
- Support for manual entry, file upload, or JSON input
- Automatic vector creation and storage

#### 🔍 Vector Search Tab
- Semantic search across stored vectors
- Configurable number of results
- Namespace support for organized storage

#### 🗄️ Vector Management Tab
- View index statistics
- List available models
- Manage vector database

#### 📈 Analytics Tab
- Run example demonstrations
- View performance metrics
- Test functionality

## Configuration Options

### API Keys
- **OpenAI API Key**: Required for text embedding generation
- **Pinecone API Key**: Required for vector database operations

### Model Settings
- **Embedding Model**: Choose from available OpenAI embedding models
- **Index Name**: Specify the Pinecone index to use
- **Vector Dimension**: Set the dimension of embedding vectors

## Input Methods

### Manual Entry
- Enter multiple texts manually through the interface
- Specify custom IDs for each text

### File Upload
- **Text Files**: One text per line
- **CSV Files**: First column as ID, second column as text
- **JSON Files**: Structured data with id and text fields

### JSON Input
- Paste JSON data directly into the interface
- Support for both single objects and arrays

## Example Usage

1. **Configure API Keys**: Enter your OpenAI and Pinecone API keys in the sidebar
2. **Generate Embeddings**: Use the Text Embedding tab to create embeddings for individual texts
3. **Batch Process**: Use the Batch Processing tab to process multiple texts at once
4. **Search Vectors**: Use the Vector Search tab to find similar content
5. **Manage Data**: Use the Vector Management tab to view statistics and manage your vector database

## Error Handling

The interface includes comprehensive error handling:
- API key validation
- Network error handling
- Input validation
- User-friendly error messages

## Dependencies

- `streamlit`: Web interface framework
- `openai`: OpenAI API client
- `pinecone`: Pinecone vector database client
- `pandas`: Data manipulation
- `numpy`: Numerical operations

## Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure both OpenAI and Pinecone API keys are valid
2. **Index Not Found**: Check that the specified Pinecone index exists
3. **Dimension Mismatch**: Ensure the vector dimension matches your embedding model
4. **Rate Limits**: Be aware of API rate limits for both OpenAI and Pinecone

### Getting Help
- Check the console output for detailed error messages
- Verify your API keys and permissions
- Ensure your Pinecone index is properly configured
