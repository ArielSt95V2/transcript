# python -m streamlit run database/UIs/streamlit_app.py

import streamlit as st
from database.utils import get_youtube_transcript


def main():
    st.set_page_config(
        page_title="YouTube Transcript Extractor",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("📝 YouTube Transcript Extractor")
    st.markdown("Extract transcripts from YouTube videos easily!")
    
    # Input section
    st.header("Enter YouTube Video URL")
    video_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste any YouTube video URL here"
    )
    
    # Extract button
    if st.button("Extract Transcript", type="primary"):
        if video_url:
            with st.spinner("Extracting transcript..."):
                transcript = get_youtube_transcript(video_url)
            
            if transcript.startswith("Invalid") or transcript.startswith("Error"):
                st.error(transcript)
            else:
                st.success("Transcript extracted successfully!")
                
                # Display transcript
                st.header("📄 Transcript")
                st.text_area(
                    "Transcript Content",
                    value=transcript,
                    height=400,
                    help="You can copy this text or download it"
                )
                
                # Download button
                st.download_button(
                    label="📥 Download Transcript",
                    data=transcript,
                    file_name="youtube_transcript.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter a YouTube URL first!")
    
    # Instructions
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Copy a YouTube URL** from any video you want to extract the transcript from
    2. **Paste the URL** in the input field above
    3. **Click "Extract Transcript"** to get the transcript
    4. **Copy or download** the transcript text
    
    **Supported URL formats:**
    - `https://www.youtube.com/watch?v=VIDEO_ID`
    - `https://youtu.be/VIDEO_ID`
    - `https://www.youtube.com/embed/VIDEO_ID`
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
