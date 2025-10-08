# Transcript & Embedding Tools

A comprehensive Django application with Streamlit UIs for YouTube transcript extraction and text embedding operations.

## Features

### 📝 YouTube Transcript Extractor
- Extract transcripts from YouTube videos
- Support for various YouTube URL formats
- Download transcripts as text files
- Simple, user-friendly interface

### 🧠 Embedding Utility Interface
- Generate text embeddings using OpenAI
- Store and query vectors in Pinecone vector database
- Batch processing capabilities
- Semantic search functionality
- Interactive vector management

## Quick Start

### Prerequisites
1. Install dependencies:
   ```bash
   pip install -r req.txt
   ```

2. Set up environment variables in `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

### Running the Applications

#### Option 1: Use the Main Launcher
```bash
python -m streamlit run database/UIs/main_ui.py
```

#### Option 2: Run Individual Applications
- **YouTube Transcript Extractor:**
  ```bash
  python -m streamlit run database/UIs/streamlit_app.py
  ```

- **Embedding Utility Interface:**
  ```bash
  python -m streamlit run database/UIs/embedding_ui.py
  ```

#### Option 3: Django API Server
```bash
python manage.py runserver
```

## Project Structure

```
transcript/
├── config/                 # Django configuration
├── database/              # Main Django app
│   ├── UIs/              # Streamlit interfaces
│   │   ├── main_ui.py           # Main launcher
│   │   ├── streamlit_app.py     # YouTube extractor
│   │   ├── embedding_ui.py      # Embedding utility
│   │   └── EMBEDDING_UI_README.md
│   ├── utils/            # Utility modules
│   │   ├── embed.py      # EmbeddingUtility class
│   │   └── llm_analyze.py
│   ├── models.py         # Django models
│   ├── views.py          # API views
│   └── serializers.py    # API serializers
├── media/                # Uploaded files
├── BACKEND_FEATURE_WORKFLOW.md  # Backend development guide
└── req.txt              # Dependencies
```

## Available Tools

### 1. YouTube Transcript Extractor (`streamlit_app.py`)
- **Purpose**: Extract transcripts from YouTube videos
- **Features**:
  - Support for multiple YouTube URL formats
  - Real-time transcript extraction
  - Download functionality
  - Error handling for invalid URLs

### 2. Embedding Utility Interface (`embedding_ui.py`)
- **Purpose**: Comprehensive interface for text embedding operations
- **Features**:
  - Single text embedding generation
  - Batch text processing
  - Vector database management
  - Semantic search capabilities
  - Multiple input methods (manual, file upload, JSON)
  - Real-time configuration

### 3. Main Launcher (`main_ui.py`)
- **Purpose**: Central hub for accessing all tools
- **Features**:
  - Quick access to all applications
  - Setup instructions
  - Feature overview

## API Endpoints

The Django backend provides REST API endpoints for programmatic access:

- `GET /api/transcripts/` - List all transcripts
- `POST /api/transcripts/` - Create new transcript
- `GET /api/transcripts/{id}/` - Get specific transcript
- `PUT /api/transcripts/{id}/` - Update transcript
- `DELETE /api/transcripts/{id}/` - Delete transcript

## Development Documentation

For developers contributing to or extending the backend:

### Backend Feature Development
See [BACKEND_FEATURE_WORKFLOW.md](BACKEND_FEATURE_WORKFLOW.md) for:
- Complete coding standards for models, serializers, views, and URLs
- Step-by-step workflow for adding new features
- Example implementations with best practices
- Common patterns and troubleshooting

This comprehensive guide covers the full lifecycle of backend feature development, from model definition through testing.

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### Model Configuration
- **Embedding Model**: `text-embedding-3-large` (default)
- **Vector Dimension**: 3072 (for text-embedding-3-large)
- **Pinecone Index**: `learning-assistant` (default)

## Dependencies

Key dependencies include:
- `django`: Web framework
- `streamlit`: UI framework
- `openai`: OpenAI API client
- `pinecone`: Vector database client
- `youtube-transcript-api`: YouTube transcript extraction
- `pandas`: Data manipulation
- `numpy`: Numerical operations

## Usage Examples

### Extract YouTube Transcript
1. Run the YouTube extractor: `python -m streamlit run database/UIs/streamlit_app.py`
2. Paste a YouTube URL
3. Click "Extract Transcript"
4. Copy or download the result

### Generate Text Embeddings
1. Run the embedding utility: `python -m streamlit run database/UIs/embedding_ui.py`
2. Configure API keys in the sidebar
3. Use the "Text Embedding" tab for single texts
4. Use the "Batch Processing" tab for multiple texts
5. Use the "Vector Search" tab to find similar content

## Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure both OpenAI and Pinecone API keys are valid
2. **Index Not Found**: Check that the specified Pinecone index exists
3. **Dimension Mismatch**: Ensure vector dimensions match your embedding model
4. **Rate Limits**: Be aware of API rate limits

### Getting Help
- Check console output for detailed error messages
- Verify API keys and permissions
- Ensure proper environment setup

## License

This project is open source and available under the MIT License.
