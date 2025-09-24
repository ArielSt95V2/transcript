# Complete CRUD Testing Collection

## Overview
Comprehensive Postman collection testing all CRUD operations for ModelViewSets with both ID and name-based lookups.

## Collection
- **File**: `complete_crud_testing_collection.json`
- **Base URL**: `http://localhost:8000`

## Endpoints Tested
- Topics: `/api/topics/`
- Information Sources: `/api/information-sources/`
- User Questions: `/api/user-questions/`
- Knowledge Nodes: `/api/knowledge-nodes/`
- Transcript Extraction: `/api/extract-transcript/`

## Test Coverage (43 Total)
- **Topics CRUD**: 9 tests (ID + name-based)
- **Information Sources CRUD**: 9 tests (ID + identifier-based)
- **User Questions CRUD**: 9 tests (ID + text-based)
- **Knowledge Nodes CRUD**: 9 tests (ID + concept-based)
- **Error Testing**: 4 tests (validation + 404)
- **Transcript Extraction**: 3 tests

## Environment Variables
| Variable | Default Value |
|----------|---------------|
| `{{base_url}}` | `http://localhost:8000` |
| `{{topic_id}}` | `1` |
| `{{topic_name}}` | `machine-learning` |
| `{{info_source_id}}` | `1` |
| `{{info_source_identifier}}` | `dQw4w9WgXcQ` |
| `{{user_question_id}}` | `1` |
| `{{user_question_text}}` | `what-is-machine-learning` |
| `{{knowledge_node_id}}` | `1` |
| `{{knowledge_node_concept}}` | `neural-networks` |

## Usage
1. Import collection into Postman
2. Set environment variables
3. Run CREATE tests first to establish data
4. Update ID variables after creation
5. Run remaining CRUD tests

## Prerequisites
- Django server running on `http://localhost:8000`
- Database migrated: `python manage.py migrate`
- Dependencies installed

## Sample Data
```json
// Topic
{"name": "Machine Learning", "description": "Introduction to ML concepts"}

// Information Source
{"source_type": "youtube", "source_identifier": "dQw4w9WgXcQ", "raw_content": "..."}

// User Question
{"question_text": "What is machine learning?", "answer_text": "..."}

// Knowledge Node
{"concept_name": "Neural Networks", "topic": 1, "content_source": 1}
```

## Expected Responses
- **CREATE**: 201 with object data
- **LIST**: 200 with array
- **RETRIEVE**: 200 with single object
- **UPDATE**: 200 with updated object
- **DELETE**: 204 no content
- **ERROR**: 400/404 with error message
