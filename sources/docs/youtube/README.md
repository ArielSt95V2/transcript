# YouTube Transcript Sources App

This Django app provides a complete REST API for extracting, storing, and managing YouTube video transcripts.

## Overview

The `sources` app implements the YouTube transcript extraction feature following the coding standards outlined in `Plan1.md`. It provides automatic transcript extraction, storage, and retrieval through a RESTful API.

## Features

- **Automatic Transcript Extraction**: Extracts transcripts automatically when creating a new record
- **Duplicate Prevention**: Prevents duplicate transcripts based on video_id
- **Status Tracking**: Tracks extraction status (pending, success, failed)
- **Error Handling**: Stores detailed error messages for failed extractions
- **Re-extraction Support**: Custom endpoint to retry failed extractions
- **Filtering**: Filter by status, language, and video_id
- **Admin Interface**: Full Django admin interface for management

## API Endpoints

### List All Transcripts
```http
GET /api/sources/youtube-transcripts/
```

**Query Parameters:**
- `status`: Filter by status (pending, success, failed)
- `language`: Filter by language code (e.g., 'en')
- `video_id`: Search by video ID

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Python Tutorial Transcript",
    "description": "Full transcript of Python basics tutorial",
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "video_id": "dQw4w9WgXcQ",
    "title": null,
    "channel_name": null,
    "language": "en",
    "status": "success",
    "status_display": "Success",
    "character_count": 15420,
    "created_at": "2025-10-08T12:00:00Z",
    "updated_at": "2025-10-08T12:01:00Z"
  }
]
```

### Create New Transcript
```http
POST /api/sources/youtube-transcripts/
```

**Request Body:**
```json
{
  "name": "Python Tutorial Transcript",
  "description": "Full transcript of Python basics tutorial",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "language": "en"
}
```

**Response:** Returns the created transcript with extraction status

**Notes:**
- Transcript extraction happens automatically on creation
- `video_id` is extracted automatically from the URL
- Duplicate video_ids are rejected with a validation error

### Get Transcript by ID
```http
GET /api/sources/youtube-transcripts/{id}/
```

**Response Example:**
```json
{
  "id": 1,
  "name": "Python Tutorial Transcript",
  "description": "Full transcript of Python basics tutorial",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "video_id": "dQw4w9WgXcQ",
  "title": null,
  "channel_name": null,
  "transcript_text": "Welcome to this Python tutorial...",
  "language": "en",
  "duration": null,
  "status": "success",
  "status_display": "Success",
  "error_message": null,
  "character_count": 15420,
  "word_count": 2840,
  "created_at": "2025-10-08T12:00:00Z",
  "updated_at": "2025-10-08T12:01:00Z"
}
```

### Get Transcript by Video ID (Name Lookup)
```http
GET /api/sources/youtube-transcripts/{video_id}/
```

Example: `GET /api/sources/youtube-transcripts/dQw4w9WgXcQ/`

### Update Transcript Metadata
```http
PATCH /api/sources/youtube-transcripts/{id}/
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "title": "Video Title",
  "channel_name": "Channel Name"
}
```

**Notes:**
- `video_url` cannot be updated after creation
- `video_id` and `status` are read-only

### Delete Transcript
```http
DELETE /api/sources/youtube-transcripts/{id}/
```

### Re-extract Transcript (Custom Action)
```http
POST /api/sources/youtube-transcripts/{id}/re_extract/
```

**Use Cases:**
- Retry failed extractions
- Update existing transcripts with latest version
- Recover from temporary errors

**Response:** Returns updated transcript with new extraction status

## Model Structure

### YouTubeTranscript Model

```python
class YouTubeTranscript(BaseModel):
    # Inherited from BaseModel:
    # - name (CharField)
    # - description (TextField)
    # - created_at (DateTimeField)
    # - updated_at (DateTimeField)
    
    video_url = URLField(max_length=500)
    video_id = CharField(max_length=20, unique=True, db_index=True)
    title = CharField(max_length=500, optional)
    channel_name = CharField(max_length=255, optional)
    transcript_text = TextField(optional)
    language = CharField(max_length=10, default='en')
    duration = DurationField(optional)
    status = CharField(choices=['pending', 'success', 'failed'])
    error_message = TextField(optional)
```

## Implementation Details

### Serializers

Following the standard pattern from `Plan1.md`, three serializers are implemented:

1. **YouTubeTranscriptListSerializer**: Lightweight for list views
   - Includes character count
   - Status display field

2. **YouTubeTranscriptDetailSerializer**: Full data for detail views
   - Includes full transcript text
   - Character and word counts
   - All metadata fields

3. **YouTubeTranscriptCreateUpdateSerializer**: For create/update operations
   - Auto-extracts video_id from URL
   - Validates URL format
   - Triggers automatic transcript extraction on create
   - Prevents duplicate video_ids

### ViewSet

`YouTubeTranscriptViewSet` inherits from `BaseNamedModelViewSet` and provides:

- Standard CRUD operations
- Query parameter filtering (status, language, video_id)
- Custom `re_extract` action for retrying extractions
- Automatic serializer selection based on action

### Transcript Extraction

The `extract_youtube_transcript()` function in `transcript.py`:

- Extracts video ID from various YouTube URL formats
- Uses `youtube-transcript-api` library
- Returns structured data with success status
- Handles errors gracefully with detailed messages

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

## Admin Interface

The Django admin interface provides:

- List view with video_id, name, status, language, created_at
- Filtering by status, language, creation date
- Search by name, video_url, video_id, title, channel_name
- Organized fieldsets for better UX
- Read-only fields for video_id, status, timestamps

## Usage Examples

### Python/Requests

```python
import requests

# Create new transcript
response = requests.post(
    'http://localhost:8000/api/sources/youtube-transcripts/',
    json={
        'name': 'My Video Transcript',
        'description': 'Transcript of my favorite video',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'language': 'en'
    }
)

transcript = response.json()
print(f"Transcript ID: {transcript['id']}")
print(f"Status: {transcript['status']}")

# Get transcript details
response = requests.get(
    f"http://localhost:8000/api/sources/youtube-transcripts/{transcript['id']}/"
)

details = response.json()
print(f"Transcript Text: {details['transcript_text'][:100]}...")

# Re-extract if failed
if details['status'] == 'failed':
    response = requests.post(
        f"http://localhost:8000/api/sources/youtube-transcripts/{transcript['id']}/re_extract/"
    )
    print(f"Re-extraction status: {response.json()['status']}")
```

### cURL

```bash
# Create transcript
curl -X POST http://localhost:8000/api/sources/youtube-transcripts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Video Transcript",
    "description": "Transcript of my favorite video",
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'

# List all successful transcripts
curl "http://localhost:8000/api/sources/youtube-transcripts/?status=success"

# Get by video ID
curl http://localhost:8000/api/sources/youtube-transcripts/dQw4w9WgXcQ/

# Re-extract transcript
curl -X POST http://localhost:8000/api/sources/youtube-transcripts/1/re_extract/
```

## Error Handling

### Common Errors

**Invalid YouTube URL:**
```json
{
  "video_url": [
    "Invalid YouTube URL format. Please provide a valid YouTube video URL."
  ]
}
```

**Duplicate Video ID:**
```json
{
  "non_field_errors": [
    "A transcript for video ID 'dQw4w9WgXcQ' already exists."
  ]
}
```

**Extraction Failed:**
- Status is set to 'failed'
- Error message is stored in `error_message` field
- Can be retried using the `re_extract` endpoint

## Testing

### Test Extraction

```python
from sources.transcript import extract_youtube_transcript

# Test extraction
result = extract_youtube_transcript('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

if result['success']:
    print(f"Video ID: {result['video_id']}")
    print(f"Transcript: {result['transcript_text'][:100]}...")
else:
    print(f"Error: {result['error']}")
```

### Test API Endpoints

```bash
# Run Django tests
python manage.py test sources

# Or manually test all endpoints
python manage.py shell
```

## Dependencies

- `django` - Web framework
- `djangorestframework` - REST API framework
- `youtube-transcript-api` - YouTube transcript extraction

## Future Enhancements

Potential improvements to consider:

1. **Async Processing**: Move transcript extraction to background tasks using Celery
2. **Multiple Languages**: Support for extracting transcripts in multiple languages
3. **Video Metadata**: Extract and store video title, duration, channel from YouTube API
4. **Caching**: Add caching layer for frequently accessed transcripts
5. **Rate Limiting**: Implement rate limiting to prevent API abuse
6. **Webhooks**: Add webhook support for transcript extraction completion
7. **Batch Operations**: Support bulk transcript extraction from multiple URLs

## Troubleshooting

**Issue**: Transcript extraction fails with "No transcript available"
- **Solution**: The video may not have captions. Check if captions are available on YouTube.

**Issue**: "Module openai not found" error
- **Solution**: This is a dependency in the database app. Install with `pip install openai` or use `--skip-checks` flag.

**Issue**: Duplicate video_id error when creating transcript
- **Solution**: A transcript for this video already exists. Use the existing one or delete it first.

## Contributing

When extending this app:

1. Follow the coding standards in `Plan1.md`
2. Maintain the three-serializer pattern
3. Use `BaseNamedModelViewSet` for consistency
4. Add appropriate validation
5. Update this README with new features

## License

This app is part of the transcript-full project and follows the same license.

