# YouTube Transcript Extractor API - Testing Documentation

## Overview
Postman collection for testing YouTube transcript extraction endpoint with automatic database saving.

## Collection
- **File**: `transcript_tests.json`
- **Base URL**: `http://localhost:8000`

## Endpoint
- **URL**: `POST /api/extract-transcript/`
- **Purpose**: Extract YouTube transcripts and save to InformationSource model

## Test Cases (3 Total)
- **Extract YouTube Transcript** - Valid URL extraction
- **Invalid YouTube URL** - Error handling for invalid URLs
- **Missing Video URL** - Error handling for missing parameter

## Environment Variables
| Variable | Default Value |
|----------|---------------|
| `{{base_url}}` | `http://localhost:8000` |

## Request Format
```json
{
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

## Expected Responses
### Success (200 OK)
```json
{
    "transcript": "Never gonna give you up, never gonna let you down...",
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "video_id": "dQw4w9WgXcQ",
    "saved_id": 1,
    "message": "Transcript extracted and saved successfully"
}
```

### Error (400 Bad Request)
```json
{
    "error": "video_url is required"
}
```

## Supported URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Database Impact
Creates InformationSource record:
- **source_type**: `'youtube'`
- **source_identifier**: Video ID
- **raw_content**: Full transcript text

## Prerequisites
- Django server running on `http://localhost:8000`
- Database migrated: `python manage.py migrate`
- `youtube-transcript-api` installed

## Usage
1. Import collection into Postman
2. Set `{{base_url}}` variable
3. Run tests with valid YouTube URLs
4. Check database for saved transcripts
