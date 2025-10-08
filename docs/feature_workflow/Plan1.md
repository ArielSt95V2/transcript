# Backend Feature Workflow Template

## Identified Coding Standards

### 1. Model Standards (`models.py`)

- **Inheritance**: All models inherit from `BaseModel` abstract class
- **Common fields**: name, description, created_at, updated_at (inherited)
- **String representation**: Define `__str__()` returning meaningful identifier
- **Meta class**: Include `verbose_name`, optionally `ordering`
- **Relationships**:
  - ForeignKey: Always specify `related_name`, `on_delete=models.CASCADE`
  - ManyToManyField: Use `blank=True`, specify `related_name`
- **Optional fields**: Use `blank=True, null=True`
- **Choices**: Define as lists/tuples within the model class
- **Example pattern**:
```python
class NewModel(BaseModel):
    related_field = models.ForeignKey(OtherModel, on_delete=models.CASCADE, related_name='new_models')
    choice_field = models.CharField(max_length=20, choices=CHOICES)
    optional_field = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.related_field.name})"
    
    class Meta:
        verbose_name = "New Model"
        ordering = ['name']
```


### 2. Serializer Standards (`serializers.py`)

- **Three serializers per model**:

  1. `{Model}ListSerializer` - lightweight, includes counts via SerializerMethodField
  2. `{Model}DetailSerializer` - full data with nested List serializers
  3. `{Model}CreateUpdateSerializer` - for create/update operations

- **Inheritance**: All inherit from `BaseModelSerializer`
- **Read-only fields**: Always include `['id', 'created_at', 'updated_at']`
- **Validation**: 
  - `validate_name()`: minimum 2 characters, strip whitespace
  - `validate()`: cross-field validation
- **Nested data**: Use List serializers to avoid deep nesting
- **Display fields**: Use `source='get_field_display'` for choice fields

### 3. ViewSet Standards (`views.py`)

- **Inheritance**: All viewsets inherit from `BaseNamedModelViewSet`
- **Required attributes**:
  - `queryset = Model.objects.all()`
  - `list_serializer_class`
  - `detail_serializer_class`
  - `create_update_serializer_class`
- **Filtering**: Override `get_queryset()` for query parameter filtering
- **Permissions**: Uses `AllowAny` (inherited from base)
- **Lookup**: Supports both ID and name lookup (inherited behavior)

### 4. URL Standards (`urls.py`)

- Use `DefaultRouter` from rest_framework.routers
- Register with lowercase plural endpoint names
- Import all viewsets in the views import section

### 5. Migration Standards

- Auto-generated using `python manage.py makemigrations`
- Review before applying with `python manage.py migrate`

### 6. Testing Standards

Comprehensive testing is essential for all new features. Two types of test files are required:

#### A. Python Test Script (`test_api_endpoints.py`)

**File Structure**:
- Standalone script with zero Django test framework dependencies
- Uses `requests` library for HTTP calls
- Color-coded terminal output using ANSI codes
- Centralized configuration (BASE_URL, API_BASE)
- Test results tracking in global dictionary

**Required Components**:

1. **Configuration Section**:
```python
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api/appname/endpoint"
TEST_DATA = {...}  # Test fixtures
```

2. **Helper Functions**:
```python
class Colors:
    """ANSI color codes"""
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.OKGREEN}[OK] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}[INFO] {message}{Colors.ENDC}")

def print_test(test_name):
    print(f"{Colors.OKCYAN}{Colors.BOLD}[TEST] {test_name}{Colors.ENDC}")
```

3. **Test Tracking Decorator**:
```python
test_results = {
    'passed': 0,
    'failed': 0,
    'total': 0,
    'resource_id': None  # Track created resource IDs
}

@run_test
def run_test(test_func):
    def wrapper(*args, **kwargs):
        test_results['total'] += 1
        try:
            result = test_func(*args, **kwargs)
            if result:
                test_results['passed'] += 1
            else:
                test_results['failed'] += 1
            return result
        except Exception as e:
            test_results['failed'] += 1
            print_error(f"Test failed with exception: {str(e)}")
            return None
    return wrapper
```

4. **Test Naming Convention**:
```python
@run_test
def test_01_list_empty_resources():
    """Test 1: GET /api/resources/ - Initial list (may be empty)"""
    print_test("List all resources (initial state)")
    
    response = requests.get(f"{API_BASE}/")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved {len(data)} resource(s)")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        return False
```

**Test Organization**:
- Number tests sequentially: `test_01_`, `test_02_`, etc.
- Happy path tests first (CRUD operations)
- Error handling tests second (validation, duplicates)
- Filtering and custom actions last
- Always include cleanup tests (delete created resources)

**Required Test Coverage**:
1. ✅ List all resources (empty/populated)
2. ✅ Create new resource (valid data)
3. ✅ Create duplicate (should fail with 400)
4. ✅ Create with invalid data (should fail with 400)
5. ✅ Get resource by ID
6. ✅ Get resource by name (if supported)
7. ✅ List all resources (verify creation)
8. ✅ Filter by each query parameter
9. ✅ Update resource metadata
10. ✅ Custom actions (if any)
11. ✅ Delete resource
12. ✅ Verify deletion (should 404)

**Summary Reporting**:
```python
def print_summary():
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    
    print(f"\n{'='*80}")
    print(f"  Total Tests: {total}")
    print(f"  {Colors.OKGREEN}Passed: {passed}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Failed: {failed}{Colors.ENDC}")
    
    if failed == 0:
        print(f"\n  {Colors.OKGREEN}{Colors.BOLD}*** ALL TESTS PASSED! ***{Colors.ENDC}\n")
    else:
        print(f"\n  {Colors.WARNING}{Colors.BOLD}*** SOME TESTS FAILED ***{Colors.ENDC}\n")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"  Success Rate: {success_rate:.1f}%\n")
```

#### B. Postman Collection (`{Feature}_API.postman_collection.json`)

**File Structure**:
```json
{
  "info": {
    "_postman_id": "unique-id",
    "name": "Feature API",
    "description": "Complete API collection for Feature endpoints",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [...],
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000",
      "type": "string"
    },
    {
      "key": "resource_id",
      "value": "",
      "type": "string"
    }
  ]
}
```

**Request Organization**:
- Group by functionality (CRUD, Validation, Filtering, Custom Actions)
- Descriptive request names (e.g., "Create New Resource", "Filter by Status")
- Detailed descriptions for each request

**Automated Test Scripts**:

Every request must include test scripts:

```javascript
// Status code validation
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Response structure validation
pm.test("Response has required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData).to.have.property('name');
});

// Save variables for subsequent requests
pm.test("Save resource ID", function () {
    var jsonData = pm.response.json();
    pm.collectionVariables.set("resource_id", jsonData.id);
});

// Data validation
pm.test("Field validation", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.field_name).to.equal('expected_value');
});
```

**Required Requests**:
1. List All Resources
2. Create New Resource (with automated tests)
3. Create Duplicate (should fail - 400)
4. Create with Invalid Data (should fail - 400)
5. Get Resource by ID
6. Get Resource by Name (if supported)
7. Filter by Status/Type/etc.
8. Update Resource Metadata
9. Custom Actions (if any)
10. Delete Resource
11. Verify Deletion (should 404)

**Collection Variables**:
- `base_url`: API base URL
- `resource_id`: Created resource ID (auto-populated)
- Any other dynamic values needed across requests

#### C. Testing Documentation (`TESTING_GUIDE.md`)

**Required Sections**:

1. **Prerequisites**
   - Dependencies to install
   - Server setup
   - Environment variables

2. **Running Python Tests**
   - Step-by-step instructions
   - Expected output
   - Troubleshooting

3. **Using Postman Collection**
   - Import instructions
   - Running individual requests
   - Running collection runner

4. **Test Scenarios**
   - Happy path walkthrough
   - Error handling examples
   - Edge cases

5. **Troubleshooting**
   - Common errors and solutions
   - Connection issues
   - Data cleanup

#### Testing Best Practices

1. **Windows Compatibility**: Use ASCII symbols instead of Unicode (`[OK]` not ✓)
2. **Error Messages**: Clear, actionable error messages
3. **Data Cleanup**: Always clean up test data (delete created resources)
4. **Isolation**: Tests should not depend on external state
5. **Validation Depth**: Test both status codes AND response structure
6. **Performance**: Include response time assertions where appropriate
7. **Documentation**: Docstrings for every test explaining purpose
8. **Version Control**: Commit both test files with feature code

## Step-by-Step Workflow

### Step 1: Define the Model

**File**: `transcript/database/models.py`

1. Add model class inheriting from `BaseModel`
2. Define fields with appropriate types and options
3. Add ForeignKey/ManyToMany relationships with `related_name`
4. Define choice fields as class-level tuples/lists
5. Implement `__str__()` method
6. Add Meta class with `verbose_name` and optional `ordering`

### Step 2: Create Serializers

**File**: `transcript/database/serializers.py`

1. **List Serializer**:

   - Inherit from `BaseModelSerializer`
   - Add `_display` fields for choices using `source='get_field_display'`
   - Add count fields using `SerializerMethodField()`
   - Implement `get_*_count()` methods
   - Define fields in Meta (exclude nested relationships)

2. **Detail Serializer**:

   - Inherit from `BaseModelSerializer`
   - Add nested serializers (use List versions)
   - Include all related data
   - Add `_display` fields for choices
   - Define all fields in Meta

3. **CreateUpdate Serializer**:

   - Inherit from `BaseModelSerializer`
   - Include only editable fields
   - Add `validate_name()` method (min 2 chars, strip)
   - Add `validate()` for cross-field validation
   - Set `read_only_fields = ['id']`

### Step 3: Create ViewSet

**File**: `transcript/database/views.py`

1. Import model and serializers at the top
2. Create viewset class inheriting from `BaseNamedModelViewSet`
3. Set four class attributes (queryset, three serializer classes)
4. Override `get_queryset()` if filtering is needed
5. Add query parameter filters using `request.query_params.get()`

### Step 4: Register URL Routes

**File**: `transcript/database/urls.py`

1. Import the viewset in the import section
2. Register with router using lowercase plural name: `router.register(r'newmodels', NewModelViewSet)`

### Step 5: Create and Apply Migrations

**Commands**:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Test Files

**Files to create**:
- `{app}/test_api_endpoints.py` - Python test script
- `{app}/{Feature}_API.postman_collection.json` - Postman collection
- `{app}/TESTING_GUIDE.md` - Testing documentation

**Python Test Script (`test_api_endpoints.py`)**:

1. Create file structure:
   - Import section (requests, json, datetime)
   - Configuration (BASE_URL, API_BASE, test data)
   - Colors class for terminal output
   - Helper functions (print_success, print_error, print_test, print_info)
   - Test tracking decorator and results dict
   - Test functions (numbered test_01_, test_02_, etc.)
   - Summary function
   - Main function

2. Implement required tests:
   - Happy path: List, Create, Get, Update, Delete
   - Error handling: Duplicates, Invalid data, 404s
   - Filtering: All query parameters
   - Custom actions: Any special endpoints

3. Include cleanup:
   - Delete created test data
   - Verify deletion

**Postman Collection**:

1. Create collection with:
   - Collection info (name, description)
   - Collection variables (base_url, resource_id, etc.)
   - Organized requests (CRUD, Validation, Filtering, Custom Actions)

2. Add automated tests to each request:
   - Status code assertions
   - Response structure validation
   - Data validation
   - Variable persistence

3. Document each request:
   - Clear request names
   - Detailed descriptions
   - Example responses

**Testing Guide (`TESTING_GUIDE.md`)**:

Create comprehensive documentation covering:
- Prerequisites and setup
- Python test script usage
- Postman collection usage
- Test scenarios
- Troubleshooting

### Step 7: Run Tests and Verify

**Available endpoints** (automatically created by ViewSet):

- `GET /api/newmodels/` - List all
- `POST /api/newmodels/` - Create new
- `GET /api/newmodels/{id}/` - Retrieve by ID
- `GET /api/newmodels/{name}/` - Retrieve by name (if using BaseNamedModelViewSet)
- `PUT /api/newmodels/{id}/` - Full update
- `PATCH /api/newmodels/{id}/` - Partial update
- `DELETE /api/newmodels/{id}/` - Delete
- Custom actions: Any `@action` decorated methods

**Running Python Tests**:

```bash
# Terminal 1: Start Django server
python manage.py runserver

# Terminal 2: Run tests
cd {app_directory}
python test_api_endpoints.py
```

**Expected Results**:
- All tests should pass (100% success rate)
- Clear output showing each test result
- Summary statistics at the end
- Green success messages for passing tests
- Red error messages for failures (with details)

**Running Postman Tests**:

1. Import collection into Postman
2. Ensure Django server is running
3. Run individual requests or entire collection
4. Verify all automated tests pass
5. Check response data matches expectations

**Verification Checklist**:
- ✅ All CRUD operations work correctly
- ✅ Validation rejects invalid data
- ✅ Filtering returns correct results
- ✅ Custom actions function as expected
- ✅ Error messages are clear and helpful
- ✅ Status codes match REST conventions
- ✅ Response structure is consistent
- ✅ Test data is cleaned up properly

## Key Files to Create/Modify

### Core Feature Files:
1. `transcript/database/models.py` - Add model class
2. `transcript/database/serializers.py` - Add 3 serializers (List, Detail, CreateUpdate)
3. `transcript/database/views.py` - Add viewset class
4. `transcript/database/urls.py` - Register route with router

### Testing Files (Required):
5. `{app}/test_api_endpoints.py` - Python test script
6. `{app}/{Feature}_API.postman_collection.json` - Postman collection
7. `{app}/TESTING_GUIDE.md` - Testing documentation

### Documentation Files (Optional but Recommended):
8. `{app}/README.md` - Feature documentation
9. `{app}/IMPLEMENTATION_SUMMARY.md` - Implementation notes

## Best Practices

### Code Quality:
- Always use `related_name` for reverse relationships
- Keep serializers lightweight for list views
- Use SerializerMethodField for computed values
- Validate all user inputs in CreateUpdate serializers
- Add query parameter filtering in get_queryset() when needed
- Follow naming conventions: plural endpoints, PascalCase classes

### Testing:
- **Create tests BEFORE marking feature complete** (Step 6)
- Test both happy path and error cases
- Include all CRUD operations in tests
- Test all query parameter filters
- Verify validation works (duplicates, invalid data)
- Clean up test data after tests complete
- Document how to run tests in TESTING_GUIDE.md
- Commit test files with feature code

### Documentation:
- Add docstrings to all test functions
- Include usage examples in documentation
- Document any special requirements or edge cases
- Keep README updated with new endpoints

### Deployment:
- Run full test suite before deploying
- Verify migrations apply cleanly
- Check for linter errors
- Test on clean database state
- Update API documentation if needed