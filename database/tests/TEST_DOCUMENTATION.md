# API Endpoints Test Documentation

## Overview
This test suite provides comprehensive testing for all API endpoints in the database application. It covers all CRUD operations (Create, Read, Update, Delete) for every model.

## Test Coverage

### Models Tested
1. **Domain** - Top-level organizational unit
2. **SubDomain** - Child of Domain
3. **Phase** - Child of SubDomain
4. **Concept** - Links Domain, SubDomain, and Phase
5. **Theme** - Child of Concept
6. **Reference** - Standalone with optional SubDomain link
7. **Component** - Standalone resource
8. **Tool** - Standalone resource
9. **Technique** - Complex model with many relationships
10. **Composition** - Most complex model with all relationships

### Test Classes

#### 1. DomainAPITestCase
- ✅ List all domains
- ✅ Create domain with validation
- ✅ Retrieve by ID and by name
- ✅ Full update (PUT)
- ✅ Partial update (PATCH)
- ✅ Delete domain
- ✅ 404 handling

#### 2. SubDomainAPITestCase
- ✅ List all subdomains
- ✅ Create subdomain with parent relationship
- ✅ Validation errors
- ✅ Retrieve with nested data
- ✅ Update operations
- ✅ Delete subdomain

#### 3. PhaseAPITestCase
- ✅ List all phases
- ✅ Create phase with parent relationship
- ✅ Retrieve with nested data
- ✅ Update operations
- ✅ Delete phase

#### 4. ConceptAPITestCase
- ✅ List all concepts
- ✅ Create concept with multiple relationships
- ✅ Relationship validation (ensures Domain → SubDomain → Phase consistency)
- ✅ Retrieve with nested data
- ✅ Update operations
- ✅ Delete concept

#### 5. ThemeAPITestCase
- ✅ List all themes
- ✅ Create theme
- ✅ Retrieve with nested concept data
- ✅ Update operations
- ✅ Delete theme

#### 6. ReferenceAPITestCase
- ✅ List all references
- ✅ Create YouTube reference
- ✅ Create file-based reference
- ✅ Validation (requires URL or file path)
- ✅ Retrieve with type display
- ✅ Update operations
- ✅ Delete reference

#### 7. ComponentAPITestCase
- ✅ List all components
- ✅ Create component with type and format
- ✅ Retrieve with relationships
- ✅ Update operations
- ✅ Delete component

#### 8. ToolAPITestCase
- ✅ List all tools
- ✅ Create tool with platform and category
- ✅ Retrieve with display names
- ✅ Update operations
- ✅ Delete tool

#### 9. TechniqueAPITestCase
- ✅ List all techniques
- ✅ Create technique with many-to-many relationships
- ✅ Validation (outcome length)
- ✅ Retrieve with all nested relationships
- ✅ Add/update many-to-many relationships
- ✅ Delete technique

#### 10. CompositionAPITestCase
- ✅ List all compositions
- ✅ Create composition with complete hierarchy
- ✅ Retrieve with all relationships
- ✅ Update operations
- ✅ Delete composition

#### 11. IntegrationTestCase
- ✅ Full workflow: create complete hierarchy
- ✅ Cascade delete behavior
- ✅ Many-to-many relationship management
- ✅ Bulk operations
- ✅ Name-based lookup edge cases

## Running the Tests

### Run All Tests
```bash
# Navigate to the project directory
cd transcript-full/transcript

# Run all tests in the test file
python manage.py test database.test_api_endpoints

# Run with verbose output
python manage.py test database.test_api_endpoints --verbosity=2
```

### Run Specific Test Classes
```bash
# Test only Domain endpoints
python manage.py test database.test_api_endpoints.DomainAPITestCase

# Test only Technique endpoints
python manage.py test database.test_api_endpoints.TechniqueAPITestCase

# Test integration scenarios
python manage.py test database.test_api_endpoints.IntegrationTestCase
```

### Run Specific Test Methods
```bash
# Test a single test method
python manage.py test database.test_api_endpoints.DomainAPITestCase.test_create_domain

# Test CRUD operations for domains
python manage.py test database.test_api_endpoints.DomainAPITestCase.test_create_domain
python manage.py test database.test_api_endpoints.DomainAPITestCase.test_retrieve_domain_by_id
python manage.py test database.test_api_endpoints.DomainAPITestCase.test_update_domain_full
python manage.py test database.test_api_endpoints.DomainAPITestCase.test_delete_domain
```

### Run with Coverage
```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test database.test_api_endpoints

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in your browser
```

## Test Data Setup

Each test class uses Django's `setUp()` method to create test data before each test runs. The `BaseAPITestCase` provides:

1. **APIClient** - For making HTTP requests
2. **create_test_hierarchy()** - Creates a complete data hierarchy for complex tests
3. **assert_response_status()** - Helper for better error messages

### Sample Test Data Structure
```python
Domain "Test Domain"
  └── SubDomain "Test SubDomain"
      └── Phase "Test Phase"
          ├── Concept "Test Concept"
          │   └── Theme "Test Theme"
          └── Technique "Test Technique"
              ├── themes: [Test Theme]
              ├── tools: [Test Tool]
              ├── components: [Test Component]
              └── references: [Test Reference]
```

## Key Features Tested

### 1. CRUD Operations
Every endpoint is tested for:
- **Create** (POST): Creating new resources
- **Read** (GET): Listing and retrieving resources
- **Update** (PUT/PATCH): Full and partial updates
- **Delete** (DELETE): Removing resources

### 2. Validation
- Field length validation (e.g., name must be at least 2 characters)
- Required field validation
- Relationship consistency validation
- Custom business logic validation

### 3. Lookup Methods
- Lookup by ID: `/api/domains/1/`
- Lookup by name: `/api/domains/filmmaking/`

### 4. Nested Relationships
- Verifies that detail views include related data
- Tests many-to-many relationships
- Tests foreign key relationships
- Tests cascade delete behavior

### 5. Edge Cases
- 404 handling for non-existent resources
- Validation errors
- Mismatched relationships
- Bulk operations
- Numeric names that could be confused with IDs

## Expected Test Results

When all tests pass, you should see output like:
```
Found 60+ test methods
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....................................................................
----------------------------------------------------------------------
Ran 60+ tests in X.XXXs

OK
Destroying test database for alias 'default'...
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that Django REST Framework is installed

2. **Database Errors**
   - Django automatically creates and destroys a test database
   - Ensure your database settings are correct in `settings.py`

3. **URL Reverse Errors**
   - Verify that `urls.py` has the correct router configuration
   - Check that viewset names match the router registration

4. **Test Failures**
   - Check the error message carefully
   - Use `--verbosity=2` for more detailed output
   - Add print statements in tests for debugging

### Debug Individual Tests
```python
# Add to any test method for debugging
def test_something(self):
    response = self.client.get(url)
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    self.assertEqual(response.status_code, 200)
```

## Extending the Tests

### Adding New Test Cases
```python
def test_new_scenario(self):
    """Test description"""
    # Setup
    data = {...}
    
    # Execute
    url = reverse('endpoint-name')
    response = self.client.post(url, data, format='json')
    
    # Assert
    self.assert_response_status(response, status.HTTP_201_CREATED)
    # Add more assertions...
```

### Testing Custom Endpoints
If you add custom endpoints beyond the standard ModelViewSet:
```python
def test_custom_endpoint(self):
    url = reverse('custom-action')  # or url = '/api/custom-url/'
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
```

## Best Practices

1. **Isolation**: Each test is independent and doesn't affect others
2. **Clear Names**: Test method names clearly describe what they test
3. **Single Assertion Focus**: Each test focuses on one aspect
4. **Complete Coverage**: All CRUD operations are tested
5. **Edge Cases**: Validation and error conditions are tested
6. **Documentation**: Each test has a docstring explaining its purpose

## Performance

- The test suite creates and destroys test data for each test
- Django uses an in-memory SQLite database for testing (fast)
- Running the full suite should take less than 1 minute
- Use `--parallel` flag for faster execution on multi-core systems:
  ```bash
  python manage.py test database.test_api_endpoints --parallel
  ```

## CI/CD Integration

To integrate with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python manage.py test database.test_api_endpoints --verbosity=2
    
# Example GitLab CI
test:
  script:
    - python manage.py test database.test_api_endpoints --verbosity=2
```

## Next Steps

After running these tests:

1. ✅ Verify all tests pass
2. ✅ Check test coverage (aim for >90%)
3. ✅ Add tests for any custom logic
4. ✅ Set up continuous integration
5. ✅ Add performance/load tests if needed

## Support

For issues or questions:
1. Check Django testing documentation: https://docs.djangoproject.com/en/stable/topics/testing/
2. Check Django REST Framework testing: https://www.django-rest-framework.org/api-guide/testing/
3. Review the test file comments for specific test details

