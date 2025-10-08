"""
Standalone API Endpoint Test Script for YouTube Transcript Sources
Run this script to test all YouTube Transcript API endpoints

Usage:
    python test_api_endpoints.py

Requirements:
    pip install requests
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api/sources/youtube-transcripts"

# Test data
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
TEST_VIDEO_URL_2 = "https://www.youtube.com/watch?v=jNQXAC9IVRw"


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")


def print_test(test_name):
    """Print test name"""
    print(f"{Colors.OKCYAN}{Colors.BOLD}[TEST] {test_name}{Colors.ENDC}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}[OK] {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.OKBLUE}[INFO] {message}{Colors.ENDC}")


def print_response(response, show_full=False):
    """Print formatted response"""
    print(f"\n  Status Code: {response.status_code}")
    try:
        data = response.json()
        if show_full:
            print(f"  Response Body:\n{json.dumps(data, indent=2)}")
        else:
            # Show abbreviated response
            if isinstance(data, list):
                print(f"  Response: List with {len(data)} items")
                if data:
                    print(f"  First Item: {json.dumps(data[0], indent=2)[:200]}...")
            elif isinstance(data, dict):
                keys = list(data.keys())
                print(f"  Response Keys: {keys}")
                print(f"  Sample Data: {json.dumps({k: data[k] for k in keys[:3]}, indent=2)}")
    except:
        print(f"  Response Text: {response.text[:200]}")
    print()


# Test Results Storage
test_results = {
    'passed': 0,
    'failed': 0,
    'total': 0,
    'transcript_id': None,
    'video_id': None
}


def run_test(test_func):
    """Decorator to run and track test results"""
    def wrapper(*args, **kwargs):
        test_results['total'] += 1
        try:
            result = test_func(*args, **kwargs)
            if result:
                test_results['passed'] += 1
                return result
            else:
                test_results['failed'] += 1
                return None
        except Exception as e:
            test_results['failed'] += 1
            print_error(f"Test failed with exception: {str(e)}")
            return None
    return wrapper


@run_test
def test_01_list_empty_transcripts():
    """Test 1: GET /api/sources/youtube-transcripts/ (should be empty initially)"""
    print_test("List all transcripts (initial - should be empty or existing)")
    
    response = requests.get(f"{API_BASE}/")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved transcripts list ({len(data)} items)")
        return True
    else:
        print_error(f"Failed to retrieve transcripts. Status: {response.status_code}")
        return False


@run_test
def test_02_create_transcript():
    """Test 2: POST /api/sources/youtube-transcripts/ - Create new transcript"""
    print_test("Create new YouTube transcript")
    
    payload = {
        "name": "Test Video Transcript",
        "description": "This is a test transcript for API testing",
        "video_url": TEST_VIDEO_URL,
        "language": "en"
    }
    
    print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{API_BASE}/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, show_full=True)
    
    if response.status_code in [200, 201]:
        data = response.json()
        test_results['transcript_id'] = data.get('id')
        test_results['video_id'] = data.get('video_id')
        print_success(f"Successfully created transcript. ID: {test_results['transcript_id']}, Video ID: {test_results['video_id']}")
        return True
    else:
        print_error(f"Failed to create transcript. Status: {response.status_code}")
        return False


@run_test
def test_03_create_duplicate_transcript():
    """Test 3: POST /api/sources/youtube-transcripts/ - Try to create duplicate (should fail)"""
    print_test("Attempt to create duplicate transcript (should fail)")
    
    payload = {
        "name": "Duplicate Test",
        "description": "This should fail",
        "video_url": TEST_VIDEO_URL,
        "language": "en"
    }
    
    response = requests.post(
        f"{API_BASE}/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, show_full=True)
    
    if response.status_code == 400:
        print_success("Correctly rejected duplicate video_id")
        return True
    else:
        print_error(f"Should have rejected duplicate. Status: {response.status_code}")
        return False


@run_test
def test_04_create_invalid_url():
    """Test 4: POST /api/sources/youtube-transcripts/ - Invalid URL (should fail)"""
    print_test("Create transcript with invalid URL (should fail)")
    
    payload = {
        "name": "Invalid URL Test",
        "description": "Testing invalid URL validation",
        "video_url": "https://not-youtube.com/video",
        "language": "en"
    }
    
    response = requests.post(
        f"{API_BASE}/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, show_full=True)
    
    if response.status_code == 400:
        print_success("Correctly rejected invalid YouTube URL")
        return True
    else:
        print_error(f"Should have rejected invalid URL. Status: {response.status_code}")
        return False


@run_test
def test_05_get_transcript_by_id():
    """Test 5: GET /api/sources/youtube-transcripts/{id}/ - Get by ID"""
    if not test_results['transcript_id']:
        print_error("Skipping - No transcript ID available")
        return False
    
    print_test(f"Get transcript by ID: {test_results['transcript_id']}")
    
    response = requests.get(f"{API_BASE}/{test_results['transcript_id']}/")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved transcript. Status: {data.get('status')}")
        return True
    else:
        print_error(f"Failed to retrieve transcript. Status: {response.status_code}")
        return False


@run_test
def test_06_get_transcript_by_video_id():
    """Test 6: GET /api/sources/youtube-transcripts/{video_id}/ - Get by video ID"""
    if not test_results['video_id']:
        print_error("Skipping - No video ID available")
        return False
    
    print_test(f"Get transcript by video ID: {test_results['video_id']}")
    
    response = requests.get(f"{API_BASE}/{test_results['video_id']}/")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully retrieved transcript by video ID. Name: {data.get('name')}")
        return True
    else:
        print_error(f"Failed to retrieve transcript by video ID. Status: {response.status_code}")
        return False


@run_test
def test_07_list_all_transcripts():
    """Test 7: GET /api/sources/youtube-transcripts/ - List all (should have at least 1)"""
    print_test("List all transcripts (should have at least 1)")
    
    response = requests.get(f"{API_BASE}/")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if len(data) >= 1:
            print_success(f"Successfully retrieved {len(data)} transcript(s)")
            return True
        else:
            print_error("Expected at least 1 transcript")
            return False
    else:
        print_error(f"Failed to retrieve transcripts. Status: {response.status_code}")
        return False


@run_test
def test_08_filter_by_status_success():
    """Test 8: GET /api/sources/youtube-transcripts/?status=success - Filter by status"""
    print_test("Filter transcripts by status=success")
    
    response = requests.get(f"{API_BASE}/?status=success")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully filtered by status. Found {len(data)} successful transcript(s)")
        return True
    else:
        print_error(f"Failed to filter. Status: {response.status_code}")
        return False


@run_test
def test_09_filter_by_status_failed():
    """Test 9: GET /api/sources/youtube-transcripts/?status=failed - Filter by status"""
    print_test("Filter transcripts by status=failed")
    
    response = requests.get(f"{API_BASE}/?status=failed")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully filtered by status. Found {len(data)} failed transcript(s)")
        return True
    else:
        print_error(f"Failed to filter. Status: {response.status_code}")
        return False


@run_test
def test_10_filter_by_language():
    """Test 10: GET /api/sources/youtube-transcripts/?language=en - Filter by language"""
    print_test("Filter transcripts by language=en")
    
    response = requests.get(f"{API_BASE}/?language=en")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully filtered by language. Found {len(data)} transcript(s)")
        return True
    else:
        print_error(f"Failed to filter. Status: {response.status_code}")
        return False


@run_test
def test_11_update_transcript():
    """Test 11: PATCH /api/sources/youtube-transcripts/{id}/ - Update transcript metadata"""
    if not test_results['transcript_id']:
        print_error("Skipping - No transcript ID available")
        return False
    
    print_test(f"Update transcript metadata: {test_results['transcript_id']}")
    
    payload = {
        "name": "Updated Test Transcript",
        "description": "Updated description via API test",
        "title": "Sample Video Title",
        "channel_name": "Test Channel"
    }
    
    print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.patch(
        f"{API_BASE}/{test_results['transcript_id']}/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('name') == payload['name']:
            print_success("Successfully updated transcript metadata")
            return True
        else:
            print_error("Update did not apply correctly")
            return False
    else:
        print_error(f"Failed to update transcript. Status: {response.status_code}")
        return False


@run_test
def test_12_re_extract_transcript():
    """Test 12: POST /api/sources/youtube-transcripts/{id}/re_extract/ - Re-extract transcript"""
    if not test_results['transcript_id']:
        print_error("Skipping - No transcript ID available")
        return False
    
    print_test(f"Re-extract transcript: {test_results['transcript_id']}")
    
    response = requests.post(f"{API_BASE}/{test_results['transcript_id']}/re_extract/")
    print_response(response, show_full=True)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Successfully re-extracted transcript. Status: {data.get('status')}")
        return True
    else:
        print_error(f"Failed to re-extract transcript. Status: {response.status_code}")
        return False


@run_test
def test_13_delete_transcript():
    """Test 13: DELETE /api/sources/youtube-transcripts/{id}/ - Delete transcript"""
    if not test_results['transcript_id']:
        print_error("Skipping - No transcript ID available")
        return False
    
    print_test(f"Delete transcript: {test_results['transcript_id']}")
    
    response = requests.delete(f"{API_BASE}/{test_results['transcript_id']}/")
    print_response(response)
    
    if response.status_code == 204:
        print_success("Successfully deleted transcript")
        return True
    else:
        print_error(f"Failed to delete transcript. Status: {response.status_code}")
        return False


@run_test
def test_14_verify_deletion():
    """Test 14: GET /api/sources/youtube-transcripts/{id}/ - Verify deletion (should 404)"""
    if not test_results['transcript_id']:
        print_error("Skipping - No transcript ID available")
        return False
    
    print_test(f"Verify transcript deletion: {test_results['transcript_id']}")
    
    response = requests.get(f"{API_BASE}/{test_results['transcript_id']}/")
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returns 404 for deleted transcript")
        return True
    else:
        print_error(f"Should return 404. Got: {response.status_code}")
        return False


def print_summary():
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    
    print(f"  Total Tests: {total}")
    print(f"  {Colors.OKGREEN}Passed: {passed}{Colors.ENDC}")
    print(f"  {Colors.FAIL}Failed: {failed}{Colors.ENDC}")
    
    if failed == 0:
        print(f"\n  {Colors.OKGREEN}{Colors.BOLD}*** ALL TESTS PASSED! ***{Colors.ENDC}\n")
    else:
        print(f"\n  {Colors.WARNING}{Colors.BOLD}*** SOME TESTS FAILED ***{Colors.ENDC}\n")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"  Success Rate: {success_rate:.1f}%\n")


def main():
    """Main test runner"""
    print_header("YouTube Transcript API Endpoint Tests")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"API Endpoint: {API_BASE}")
    print_info(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        print_success("Server is running")
    except requests.exceptions.RequestException:
        print_error(f"Cannot connect to server at {BASE_URL}")
        print_error("Please ensure Django development server is running:")
        print_error("  python manage.py runserver")
        return
    
    # Run all tests
    test_01_list_empty_transcripts()
    test_02_create_transcript()
    test_03_create_duplicate_transcript()
    test_04_create_invalid_url()
    test_05_get_transcript_by_id()
    test_06_get_transcript_by_video_id()
    test_07_list_all_transcripts()
    test_08_filter_by_status_success()
    test_09_filter_by_status_failed()
    test_10_filter_by_language()
    test_11_update_transcript()
    test_12_re_extract_transcript()
    test_13_delete_transcript()
    test_14_verify_deletion()
    
    # Print summary
    print_summary()


if __name__ == "__main__":
    main()

