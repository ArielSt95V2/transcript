def get_youtube_transcript(video_url):
    """
    Legacy function for backward compatibility.
    Use extract_youtube_transcript() for new implementations.
    """
    result = extract_youtube_transcript(video_url)
    
    if result.get('success'):
        return result.get('transcript_text', '')
    else:
        return result.get('error', 'Unknown error occurred')


def extract_youtube_transcript(video_url):
    """
    Extract transcript from YouTube video URL.
    
    Args:
        video_url (str): YouTube video URL
    
    Returns:
        dict: {
            'success': bool,
            'video_id': str,
            'transcript_text': str,
            'error': str (if failed)
        }
    """
    import re
    from youtube_transcript_api import YouTubeTranscriptApi
    
    # Extract video ID from various YouTube URL formats
    match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", video_url)
    if not match:
        return {
            'success': False,
            'error': 'Invalid YouTube URL format.'
        }
    
    video_id = match.group(1)
    
    try:
        # Create API instance and fetch transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
        
        # Convert to raw data (list of dicts with 'text', 'start', 'duration')
        raw_data = fetched_transcript.to_raw_data()
        
        # Extract just the text from each snippet
        transcript_text = ' '.join([snippet['text'] for snippet in raw_data])
        
        return {
            'success': True,
            'video_id': video_id,
            'transcript_text': transcript_text,
            'error': None
        }

    except Exception as e:
        return {
            'success': False,
            'video_id': video_id,
            'error': str(e)
        }
    
    except Exception as e:
        return {
            'success': False,
            'video_id': video_id,
            'error': str(e)
        }


