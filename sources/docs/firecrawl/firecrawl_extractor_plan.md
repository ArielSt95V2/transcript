# Web Content Source with Firecrawl Implementation

## Overview

Create a complete backend feature to extract web content using Firecrawl API, storing markdown, HTML, and AI-extracted structured data. Following Plan1.md workflow standards.

## Implementation Steps

### 1. Model Creation

**File**: `transcript/sources/models.py`

- Add `WebContentSource` model inheriting from `BaseModel`
- Fields:
  - `source_url` - URLField(max_length=1000)
  - `title` - CharField(max_length=500, blank=True, null=True)
  - `author` - CharField(max_length=255, blank=True, null=True)
  - `publish_date` - DateField(blank=True, null=True)
  - `content_markdown` - TextField()
  - `content_html` - TextField(blank=True, null=True)
  - `extracted_json` - JSONField(blank=True, null=True)
  - `language` - CharField(max_length=10, default='en')
  - `status` - CharField with choices (pending/success/failed)
  - `error_message` - TextField(blank=True, null=True)
  - `metadata` - JSONField(blank=True, null=True) for Firecrawl metadata

### 3. Extraction Utility

**File**: `transcript/sources/firecrawl_extractor.py` (new file)

- Create `extract_web_content(url, extraction_prompt=None)` function
- Use Firecrawl SDK to scrape with formats: markdown, HTML
- Use JSON mode with AI prompt for structured extraction
- Return dict with success/error structure matching YouTube pattern
- Handle exceptions and API errors gracefully

### 4. Serializers

**File**: `transcript/sources/serializers.py`

Create three serializers:

**WebContentSourceListSerializer**:

- Lightweight for list views
- Include: id, name, source_url, title, status, status_display, character_count
- SerializerMethodField for character_count

**WebContentSourceDetailSerializer**:

- Full data including content_markdown, content_html, extracted_json
- Include metadata field
- SerializerMethodField for character_count, word_count

**WebContentSourceCreateUpdateSerializer**:

- Fields: name, description, source_url, extraction_prompt (optional)
- Validate URL format
- Check for duplicate URLs
- In `create()`: call extraction utility BEFORE saving
- Set status to 'success' or raise ValidationError on failure

### 5. ViewSet

**File**: `transcript/sources/views.py`

- Add `WebContentSourceViewSet` inheriting from `BaseNamedModelViewSet`
- Set queryset and three serializer classes
- Override `get_queryset()` for filtering by status, language
- Override `create()` for better error handling (like YouTubeTranscriptViewSet)

### 6. URL Registration

**File**: `transcript/sources/urls.py`

- Register route: `router.register(r'web-content', WebContentSourceViewSet)`

### 7. Migrations

- Run `python manage.py makemigrations sources`
- Run `python manage.py migrate sources`

### 8. Testing Files

**File**: `transcript/sources/tests/test_web_content_api.py`

- Python test script following Plan1.md standards
- Tests: list, create valid, create duplicate, create invalid URL, get by ID, filter by status, delete
- Use a simple test URL (e.g., https://example.com)
- Color-coded output with test tracking

**File**: `transcript/sources/tests/WebContent_API.postman_collection.json`

- Postman collection with automated tests
- Collection variables: base_url, resource_id
- Full CRUD coverage

**File**: `transcript/sources/tests/WEB_CONTENT_TESTING_GUIDE.md`

- Prerequisites including Firecrawl API key setup
- Running instructions for both test types
- Troubleshooting section

## Key Implementation Details

### Extraction Prompt Strategy

Use AI extraction prompts like:

```
"Extract the following from this web page: main topic, key concepts mentioned, 
author name, publication date, primary technologies or tools discussed, 
and a brief summary."
```

### Error Handling

- Network errors
- Invalid URLs
- Firecrawl API failures
- Rate limiting
- Missing content

### Status Flow

1. User submits URL → status='pending'
2. Extraction called → scrape with Firecrawl
3. Success → status='success', save all content
4. Failure → raise ValidationError (don't create record)

## Files to Create/Modify

**New Files**:

- `transcript/sources/firecrawl_extractor.py`
- `transcript/sources/tests/test_web_content_api.py`
- `transcript/sources/tests/WebContent_API.postman_collection.json`
- `transcript/sources/tests/WEB_CONTENT_TESTING_GUIDE.md`

**Modified Files**:

- `transcript/sources/models.py` (add WebContentSource model)
- `transcript/sources/serializers.py` (add 3 serializers)
- `transcript/sources/views.py` (add viewset)
- `transcript/sources/urls.py` (register route)
- `transcript/req.txt` (add firecrawl-py)
- `transcript/config/settings.py` (add API key config)