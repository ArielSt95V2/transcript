"""
Web Content Source API Test Script

This script tests all endpoints for the Web Content Source API.
Run this script with Django server running on http://127.0.0.1:8000
"""

import requests
import json
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api/sources/web-content"

# Test data
TEST_DATA = {
    "name": "Example Web Content Test",
    "description": "Test extraction of example.com content",
    "source_url": "https://example.com",
    "language": "en"
}

TEST_DATA_WITH_PROMPT = {
    "name": "Firecrawl Docs Test",
    "description": "Test extraction with custom prompt",
    "source_url": "https://docs.firecrawl.dev",
    "extraction_prompt": "Extract the main topic, key features, and any pricing information mentioned",
    "language": "en"
}

INVALID_URL_DATA = {
    "name": "Invalid URL Test",
    "description": "This should fail",
    "source_url": "not-a-valid-url",
    "language": "en"
}

# =============================================================================
# COLORS AND FORMATTING
# =============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.OKGREEN}[OK] {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}[INFO] {message}{Colors.ENDC}")

def print_test(test_name):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}[TEST] {test_name}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}[WARNING] {message}{Colors.ENDC}")

# =============================================================================
# TEST TRACKING
# =============================================================================

test_results = {
    'passed': 0,
    'failed': 0,
    'total': 0,
    'resource_id': None,
    'resource_name': None
}

def run_test(test_func):
    """Decorator to track test results"""
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

# =============================================================================
# TEST FUNCTIONS
# =============================================================================

@run_test
def test_01_list_empty_web_content():
    """Test 1: GET /api/sources/web-content/ - Initial list"""
    print_test("List all web content sources (initial state)")
    
    response = requests.get(f"{API_BASE}/")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved {len(data)} web content source(s)")
        print_info(f"Response: {json.dumps(data, indent=2)[:200]}...")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


@run_test
def test_02_create_web_content_valid():
    """Test 2: POST /api/sources/web-content/ - Create valid web content source"""
    print_test("Create new web content source with valid data")
    
    response = requests.post(f"{API_BASE}/", json=TEST_DATA)
    
    if response.status_code == 201:
        data = response.json()
        test_results['resource_id'] = data.get('id')
        test_results['resource_name'] = data.get('name')
        
        print_success(f"Successfully created web content source (ID: {data.get('id')})")
        print_info(f"Name: {data.get('name')}")
        print_info(f"URL: {data.get('source_url')}")
        print_info(f"Status: {data.get('status')}")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


@run_test
def test_03_create_duplicate_url():
    """Test 3: POST /api/sources/web-content/ - Create duplicate (should fail)"""
    print_test("Attempt to create duplicate web content source (should fail)")
    
    response = requests.post(f"{API_BASE}/", json=TEST_DATA)
    
    if response.status_code == 400:
        data = response.json()
        print_success("Correctly rejected duplicate URL")
        print_info(f"Error message: {data}")
        return True
    else:
        print_error(f"Should have failed with 400, got: {response.status_code}")
        return False


@run_test
def test_04_create_invalid_url():
    """Test 4: POST /api/sources/web-content/ - Create with invalid URL (should fail)"""
    print_test("Attempt to create web content with invalid URL (should fail)")
    
    response = requests.post(f"{API_BASE}/", json=INVALID_URL_DATA)
    
    if response.status_code == 400:
        data = response.json()
        print_success("Correctly rejected invalid URL")
        print_info(f"Error message: {data}")
        return True
    else:
        print_error(f"Should have failed with 400, got: {response.status_code}")
        return False


@run_test
def test_05_get_web_content_by_id():
    """Test 5: GET /api/sources/web-content/{id}/ - Retrieve by ID"""
    print_test("Get web content source by ID")
    
    resource_id = test_results['resource_id']
    if not resource_id:
        print_error("No resource ID available (previous test may have failed)")
        return False
    
    response = requests.get(f"{API_BASE}/{resource_id}/")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved web content source {resource_id}")
        print_info(f"Name: {data.get('name')}")
        print_info(f"URL: {data.get('source_url')}")
        print_info(f"Status: {data.get('status')}")
        print_info(f"Content length: {data.get('character_count')} chars")
        print_info(f"Word count: {data.get('word_count')} words")
        
        # Check if content was extracted
        if data.get('content_markdown'):
            print_success("Markdown content extracted successfully")
        if data.get('extracted_json'):
            print_success(f"Structured JSON extracted: {list(data.get('extracted_json', {}).keys())}")
        
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


@run_test
def test_06_get_web_content_by_name():
    """Test 6: GET /api/sources/web-content/{name}/ - Retrieve by name"""
    print_test("Get web content source by name")
    
    resource_name = test_results['resource_name']
    if not resource_name:
        print_error("No resource name available (previous test may have failed)")
        return False
    
    response = requests.get(f"{API_BASE}/{resource_name}/")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved web content source '{resource_name}'")
        print_info(f"ID: {data.get('id')}")
        print_info(f"URL: {data.get('source_url')}")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        return False


@run_test
def test_07_list_all_web_content():
    """Test 7: GET /api/sources/web-content/ - List all (should have 1)"""
    print_test("List all web content sources (should have at least 1)")
    
    response = requests.get(f"{API_BASE}/")
    
    if response.status_code == 200:
        data = response.json()
        if len(data) >= 1:
            print_success(f"Successfully retrieved {len(data)} web content source(s)")
            return True
        else:
            print_error(f"Expected at least 1 web content source, got {len(data)}")
            return False
    else:
        print_error(f"Failed. Status: {response.status_code}")
        return False


@run_test
def test_08_filter_by_status_success():
    """Test 8: GET /api/sources/web-content/?status=success - Filter by status"""
    print_test("Filter web content sources by status (success)")
    
    response = requests.get(f"{API_BASE}/?status=success")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully filtered: {len(data)} result(s) with status 'success'")
        
        # Verify all results have status 'success'
        all_success = all(item.get('status') == 'success' for item in data)
        if all_success:
            print_success("All results correctly filtered")
            return True
        else:
            print_error("Some results don't have status 'success'")
            return False
    else:
        print_error(f"Failed. Status: {response.status_code}")
        return False


@run_test
def test_09_filter_by_language():
    """Test 9: GET /api/sources/web-content/?language=en - Filter by language"""
    print_test("Filter web content sources by language")
    
    response = requests.get(f"{API_BASE}/?language=en")
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully filtered: {len(data)} result(s) with language 'en'")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        return False


@run_test
def test_10_update_web_content():
    """Test 10: PATCH /api/sources/web-content/{id}/ - Update metadata"""
    print_test("Update web content source metadata")
    
    resource_id = test_results['resource_id']
    if not resource_id:
        print_error("No resource ID available")
        return False
    
    update_data = {
        "description": "Updated description for testing"
    }
    
    response = requests.patch(f"{API_BASE}/{resource_id}/", json=update_data)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('description') == update_data['description']:
            print_success("Successfully updated web content source")
            print_info(f"New description: {data.get('description')}")
            return True
        else:
            print_error("Description was not updated")
            return False
    else:
        print_error(f"Failed. Status: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


@run_test
def test_11_delete_web_content():
    """Test 11: DELETE /api/sources/web-content/{id}/ - Delete web content source"""
    print_test("Delete web content source")
    
    resource_id = test_results['resource_id']
    if not resource_id:
        print_error("No resource ID available")
        return False
    
    response = requests.delete(f"{API_BASE}/{resource_id}/")
    
    if response.status_code == 204:
        print_success(f"Successfully deleted web content source {resource_id}")
        return True
    else:
        print_error(f"Failed. Status: {response.status_code}")
        print_error(f"Response: {response.text}")
        return False


@run_test
def test_12_verify_deletion():
    """Test 12: GET /api/sources/web-content/{id}/ - Verify deletion (should 404)"""
    print_test("Verify web content source was deleted (should 404)")
    
    resource_id = test_results['resource_id']
    if not resource_id:
        print_error("No resource ID available")
        return False
    
    response = requests.get(f"{API_BASE}/{resource_id}/")
    
    if response.status_code == 404:
        print_success("Correctly returns 404 for deleted resource")
        return True
    else:
        print_error(f"Should have returned 404, got: {response.status_code}")
        return False


# =============================================================================
# SUMMARY
# =============================================================================

def print_summary():
    """Print test summary"""
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    
    print(f"\n{'='*80}")
    print(f"{Colors.BOLD}WEB CONTENT SOURCE API TEST SUMMARY{Colors.ENDC}")
    print(f"{'='*80}")
    print(f"  Total Tests: {total}")
    print(f"  {Colors.OKGREEN}Passed: {passed}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Failed: {failed}{Colors.ENDC}")
    
    if failed == 0:
        print(f"\n  {Colors.OKGREEN}{Colors.BOLD}*** ALL TESTS PASSED! ***{Colors.ENDC}\n")
    else:
        print(f"\n  {Colors.WARNING}{Colors.BOLD}*** SOME TESTS FAILED ***{Colors.ENDC}\n")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"{'='*80}\n")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}WEB CONTENT SOURCE API TESTS{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}Base URL: {API_BASE}{Colors.ENDC}")
    print(f"{Colors.BOLD}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    # Run tests
    test_01_list_empty_web_content()
    test_02_create_web_content_valid()
    test_03_create_duplicate_url()
    test_04_create_invalid_url()
    test_05_get_web_content_by_id()
    test_06_get_web_content_by_name()
    test_07_list_all_web_content()
    test_08_filter_by_status_success()
    test_09_filter_by_language()
    test_10_update_web_content()
    test_11_delete_web_content()
    test_12_verify_deletion()
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()

