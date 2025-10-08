# Web Content Source API Testing Guide

This guide explains how to test the Web Content Source API endpoints that use Firecrawl for web scraping.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Running Python Tests](#running-python-tests)
4. [Using Postman Collection](#using-postman-collection)
5. [Test Scenarios](#test-scenarios)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- Python 3.8+
- Django (installed in virtual environment)
- `requests` library for Python tests
- Postman (for API collection tests)
- Django development server running

### Required Configuration

**Firecrawl API Key**: You must have a valid Firecrawl API key configured.

Set the API key in one of these ways:

1. **Environment Variable** (Recommended):
   ```bash
   # Windows (PowerShell)
   $env:FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
   
   # Windows (CMD)
   set FIRECRAWL_API_KEY=fc-YOUR-API-KEY
   
   # Linux/Mac
   export FIRECRAWL_API_KEY=fc-YOUR-API-KEY
   ```

2. **Django Settings**:
   Add to `transcript/config/settings.py`:
   ```python
   FIRECRAWL_API_KEY = 'fc-YOUR-API-KEY'
   ```

### Install Dependencies

If not already installed:

```bash
# Activate virtual environment
cd transcript
.\venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Install required packages
pip install requests firecrawl-py
```

---

## Setup

### 1. Start Django Development Server

```bash
cd transcript
.\venv\Scripts\activate  # Windows
python manage.py runserver
```

Server should be running at: `http://127.0.0.1:8000`

### 2. Verify API Key Configuration

Check that Firecrawl API key is properly set:

```python
# In Django shell
python manage.py shell

from django.conf import settings
import os

# Check if key is available
api_key = getattr(settings, 'FIRECRAWL_API_KEY', None) or os.environ.get('FIRECRAWL_API_KEY')
print(f"API Key configured: {bool(api_key)}")
```

---

## Running Python Tests

### Quick Start

1. **Ensure Django server is running** in one terminal
2. **Open a second terminal** and navigate to the tests directory:

```bash
cd transcript/sources/tests
python test_web_content_api.py
```

### Expected Output

```
================================================================================
WEB CONTENT SOURCE API TESTS
================================================================================
Base URL: http://127.0.0.1:8000/api/sources/web-content
Started: 2024-01-15 10:30:00
================================================================================

[TEST] List all web content sources (initial state)
[OK] Successfully retrieved 0 web content source(s)

[TEST] Create new web content source with valid data
[OK] Successfully created web content source (ID: 1)
[INFO] Name: Example Web Content Test
[INFO] URL: https://example.com
[INFO] Status: success

... (more tests) ...

================================================================================
WEB CONTENT SOURCE API TEST SUMMARY
================================================================================
  Total Tests: 12
  Passed: 12
  Failed: 0

  *** ALL TESTS PASSED! ***

  Success Rate: 100.0%
================================================================================
```

### Test Coverage

The Python test script covers:

1. ✅ List all web content sources (initial empty state)
2. ✅ Create new web content source with valid data
3. ✅ Create duplicate URL (should fail with 400)
4. ✅ Create with invalid URL format (should fail with 400)
5. ✅ Get web content source by ID
6. ✅ Get web content source by name
7. ✅ List all web content sources (verify creation)
8. ✅ Filter by status (success)
9. ✅ Filter by language
10. ✅ Update web content source metadata
11. ✅ Delete web content source
12. ✅ Verify deletion (should return 404)

---

## Using Postman Collection

### Import Collection

1. Open Postman
2. Click **Import** button
3. Select `WebContent_API.postman_collection.json`
4. Collection will appear in your workspace

### Collection Variables

The collection uses these variables:

- `base_url`: `http://127.0.0.1:8000` (API base URL)
- `resource_id`: Auto-populated after creating a resource
- `resource_name`: Auto-populated after creating a resource

### Running Individual Requests

1. **Ensure Django server is running**
2. Expand the collection folders
3. Click on any request
4. Click **Send** button
5. View response and automated test results in the **Test Results** tab

### Running Full Collection

1. Click on collection name
2. Click **Run** button
3. Select requests to run (or run all)
4. Click **Run Web Content Source API**
5. View test results summary

### Request Organization

**CRUD Operations:**
- List All Web Content Sources
- Create New Web Content Source
- Get Web Content Source by ID
- Get Web Content Source by Name
- Update Web Content Source
- Delete Web Content Source

**Validation Tests:**
- Create Duplicate URL (Should Fail)
- Create with Invalid URL (Should Fail)
- Create with Missing Name (Should Fail)

**Filtering:**
- Filter by Status (success)
- Filter by Language

---

## Test Scenarios

### Happy Path Walkthrough

1. **List initial state** → Should return empty array or existing resources
2. **Create new resource** → Firecrawl extracts content, returns 201
3. **Get by ID** → Returns full content including markdown, HTML, JSON
4. **Update metadata** → Change description, returns 200
5. **Delete resource** → Returns 204
6. **Verify deletion** → Returns 404

### Error Handling Examples

#### Duplicate URL

```json
POST /api/sources/web-content/
{
    "name": "Test",
    "source_url": "https://example.com"  // Already exists
}

Response: 400 Bad Request
{
    "source_url": "Content from this URL already exists (ID: 1, Name: 'Example Web Content Test')."
}
```

#### Invalid URL Format

```json
POST /api/sources/web-content/
{
    "name": "Test",
    "source_url": "not-a-url"
}

Response: 400 Bad Request
{
    "source_url": "Invalid URL format. URL must start with http:// or https://"
}
```

#### Missing Required Field

```json
POST /api/sources/web-content/
{
    "source_url": "https://example.com"
    // Missing "name"
}

Response: 400 Bad Request
{
    "details": {
        "name": ["This field is required."]
    }
}
```

### Edge Cases

#### Long-Running Extraction

Some websites may take longer to scrape. The Firecrawl timeout is set to 120 seconds. If extraction takes too long:

```json
Response: 400 Bad Request
{
    "source_url": "Failed to extract content: Request timeout. The page took too long to load."
}
```

#### Page Not Found

```json
Response: 400 Bad Request
{
    "source_url": "Failed to extract content: Page not found (404). Please check the URL."
}
```

#### API Rate Limit

```json
Response: 400 Bad Request
{
    "source_url": "Failed to extract content: Firecrawl API rate limit exceeded. Please try again later."
}
```

---

## Troubleshooting

### Common Issues

#### 1. "Firecrawl SDK not installed"

**Error:**
```
Failed to extract content: Firecrawl SDK not installed. Please install firecrawl-py package.
```

**Solution:**
```bash
pip install firecrawl-py
```

#### 2. "Firecrawl API key not configured"

**Error:**
```
Failed to extract content: Firecrawl API key not configured.
```

**Solution:**
Set the environment variable or add to Django settings (see [Prerequisites](#prerequisites)).

#### 3. "Invalid Firecrawl API key"

**Error:**
```
Failed to extract content: Invalid Firecrawl API key. Please check your configuration.
```

**Solution:**
- Verify your API key is correct
- Check you haven't exceeded your Firecrawl plan limits
- Visit https://firecrawl.dev to verify your account status

#### 4. Connection Refused

**Error:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solution:**
Ensure Django server is running:
```bash
python manage.py runserver
```

#### 5. Tests Pass But No Content Extracted

**Symptom:** Status is 'success' but `content_markdown` is empty

**Possible Causes:**
- The target website blocked the scraper
- Website requires authentication
- Page content is dynamically loaded (JavaScript-heavy)

**Solution:**
- Try a different test URL (example.com is reliable)
- Check Firecrawl documentation for advanced scraping options
- Use the `extraction_prompt` parameter for better AI extraction

### Data Cleanup

If you need to clean up test data:

```bash
# Django shell
python manage.py shell

from sources.models import WebContentSource
WebContentSource.objects.all().delete()
```

Or use the DELETE endpoint for individual resources.

### Checking Logs

Django logs will show detailed error messages:

```bash
# In terminal running Django server
# Look for log output when tests fail
```

---

## Performance Notes

### Typical Response Times

- **List/Get operations**: < 200ms
- **Create operation** (with Firecrawl extraction): 3-10 seconds
  - Depends on target website complexity
  - Includes network latency + AI processing
- **Update/Delete operations**: < 200ms

### Firecrawl Considerations

- **Rate Limits**: Check your Firecrawl plan limits
- **Timeout**: Default 120 seconds per extraction
- **Credits**: Each extraction consumes Firecrawl credits
- **Best Practice**: Use test URLs sparingly to conserve credits

---

## Additional Resources

- **Firecrawl Documentation**: https://docs.firecrawl.dev
- **Firecrawl Python SDK**: https://github.com/mendableai/firecrawl
- **Django REST Framework**: https://www.django-rest-framework.org
- **Postman Documentation**: https://learning.postman.com

---

## Support

For issues specific to:
- **Firecrawl API**: Contact Firecrawl support
- **This implementation**: Check Django logs and error messages
- **Test failures**: Review the troubleshooting section above

---

**Last Updated**: 2024-01-15  
**Test Script Version**: 1.0  
**Postman Collection Version**: 1.0

