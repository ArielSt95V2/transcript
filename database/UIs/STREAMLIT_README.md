# YouTube Transcript Extractor - Streamlit UI

A simple web interface for extracting transcripts from YouTube videos using Streamlit. This app integrates with the existing Django backend by importing the `get_youtube_transcript` function from `database.utils`.

## Features

- 🎥 Extract transcripts from any YouTube video
- 📝 Clean, formatted text output
- 💾 Download transcripts as text files
- 🎨 Modern, user-friendly interface
- 📱 Responsive design
- 🔗 Integrates with existing Django backend utilities

## How to Run

1. **Navigate to the project root directory:**
   ```bash
   cd transcript
   ```

2. **Activate your virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate
  
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   pip install -r req.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   python -m streamlit run database/UIs/streamlit_app.py
   ```

5. **Open your browser:**
   The app will automatically open in your default browser at `http://localhost:8501`

## Usage

1. Copy any YouTube video URL
2. Paste it into the input field
3. Click "Extract Transcript"
4. View, copy, or download the transcript

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Requirements

- Python 3.7+
- Streamlit
- youtube-transcript-api
- Django (for the backend utilities)
- Valid YouTube video with available transcript

## Architecture

This Streamlit app integrates with your existing Django project by:
- Importing the `get_youtube_transcript` function from `database.utils` using relative imports
- Running as a module with `python -m` to enable proper package resolution
- Leveraging the same YouTube transcript extraction logic used by your Django backend
- Providing a standalone web interface while maintaining code reusability

## Notes

- Only English transcripts are currently supported
- Some videos may not have transcripts available
- The app requires an internet connection to fetch transcripts
- **Important**: Run the app from the project root directory (`transcript/`) using `python -m streamlit run database/UIs/streamlit_app.py`
- The `python -m` flag enables relative imports to work properly by treating the script as part of a package
