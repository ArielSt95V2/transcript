def get_youtube_transcript(video_url):
    import re
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter

    # Extract video ID from various YouTube URL formats
    match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", video_url)
    if not match:
        return "Invalid YouTube URL format."
    video_id = match.group(1)

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en'])
        
        # Format the transcript as plain text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)

        return formatted_transcript

    except Exception as e:
        return str(e)