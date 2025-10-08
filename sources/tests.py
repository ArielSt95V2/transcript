from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import YouTubeTranscript
from .transcript import extract_youtube_transcript


class YouTubeTranscriptModelTests(TestCase):
    """Test cases for YouTubeTranscript model"""
    
    def setUp(self):
        self.transcript = YouTubeTranscript.objects.create(
            name="Test Transcript",
            description="Test description",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            video_id="dQw4w9WgXcQ",
            status="pending"
        )
    
    def test_model_creation(self):
        """Test that model is created correctly"""
        self.assertEqual(self.transcript.name, "Test Transcript")
        self.assertEqual(self.transcript.video_id, "dQw4w9WgXcQ")
        self.assertEqual(self.transcript.status, "pending")
    
    def test_model_str(self):
        """Test string representation"""
        expected = f"Test Transcript - dQw4w9WgXcQ (pending)"
        self.assertEqual(str(self.transcript), expected)
    
    def test_unique_video_id(self):
        """Test that video_id is unique"""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            YouTubeTranscript.objects.create(
                name="Duplicate",
                description="Duplicate description",
                video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                video_id="dQw4w9WgXcQ",
                status="pending"
            )


class YouTubeTranscriptUtilityTests(TestCase):
    """Test cases for transcript utility functions"""
    
    def test_video_id_extraction(self):
        """Test video ID extraction from various URL formats"""
        import re
        
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "https://www.youtube.com/v/dQw4w9WgXcQ",
        ]
        
        pattern = r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})"
        
        for url in urls:
            match = re.search(pattern, url)
            self.assertIsNotNone(match, f"Failed to extract from {url}")
            self.assertEqual(match.group(1), "dQw4w9WgXcQ")
    
    def test_invalid_url_format(self):
        """Test that invalid URLs are rejected"""
        result = extract_youtube_transcript("https://invalid-url.com")
        
        self.assertFalse(result['success'])
        self.assertIn('Invalid YouTube URL format', result['error'])


class YouTubeTranscriptAPITests(TestCase):
    """Test cases for YouTube Transcript API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.transcript = YouTubeTranscript.objects.create(
            name="Existing Transcript",
            description="Existing description",
            video_url="https://www.youtube.com/watch?v=existing123",
            video_id="existing123",
            status="success",
            transcript_text="This is a test transcript"
        )
    
    def test_list_transcripts(self):
        """Test GET /api/sources/youtube-transcripts/"""
        response = self.client.get('/api/sources/youtube-transcripts/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['video_id'], 'existing123')
    
    def test_get_transcript_detail(self):
        """Test GET /api/sources/youtube-transcripts/{id}/"""
        response = self.client.get(f'/api/sources/youtube-transcripts/{self.transcript.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['video_id'], 'existing123')
        self.assertEqual(response.data['transcript_text'], 'This is a test transcript')
    
    def test_get_by_video_id(self):
        """Test GET /api/sources/youtube-transcripts/{video_id}/"""
        response = self.client.get('/api/sources/youtube-transcripts/existing123/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['video_id'], 'existing123')
    
    def test_filter_by_status(self):
        """Test filtering by status"""
        # Create a failed transcript
        YouTubeTranscript.objects.create(
            name="Failed Transcript",
            description="Failed description",
            video_url="https://www.youtube.com/watch?v=failed123",
            video_id="failed123",
            status="failed"
        )
        
        # Filter by success
        response = self.client.get('/api/sources/youtube-transcripts/?status=success')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'success')
        
        # Filter by failed
        response = self.client.get('/api/sources/youtube-transcripts/?status=failed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'failed')
    
    def test_update_transcript_metadata(self):
        """Test PATCH /api/sources/youtube-transcripts/{id}/"""
        response = self.client.patch(
            f'/api/sources/youtube-transcripts/{self.transcript.id}/',
            {
                'name': 'Updated Name',
                'title': 'Updated Title'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        
        # Verify in database
        self.transcript.refresh_from_db()
        self.assertEqual(self.transcript.name, 'Updated Name')
    
    def test_delete_transcript(self):
        """Test DELETE /api/sources/youtube-transcripts/{id}/"""
        response = self.client.delete(f'/api/sources/youtube-transcripts/{self.transcript.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(YouTubeTranscript.objects.filter(id=self.transcript.id).exists())
    
    def test_create_with_invalid_url(self):
        """Test creating transcript with invalid URL"""
        response = self.client.post(
            '/api/sources/youtube-transcripts/',
            {
                'name': 'Invalid URL Test',
                'description': 'Testing invalid URL',
                'video_url': 'https://not-youtube.com/video'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)
    
    def test_create_duplicate_video_id(self):
        """Test that duplicate video_ids are rejected"""
        response = self.client.post(
            '/api/sources/youtube-transcripts/',
            {
                'name': 'Duplicate Test',
                'description': 'Testing duplicate',
                'video_url': 'https://www.youtube.com/watch?v=existing123'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class YouTubeTranscriptSerializerTests(TestCase):
    """Test cases for serializer validation"""
    
    def test_name_validation(self):
        """Test that name must be at least 2 characters"""
        from .serializers import YouTubeTranscriptCreateUpdateSerializer
        
        serializer = YouTubeTranscriptCreateUpdateSerializer(data={
            'name': 'A',  # Too short
            'description': 'Test',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_video_id_auto_extraction(self):
        """Test that video_id is automatically extracted from URL"""
        from .serializers import YouTubeTranscriptCreateUpdateSerializer
        
        serializer = YouTubeTranscriptCreateUpdateSerializer(data={
            'name': 'Test Video',
            'description': 'Test description',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        })
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['video_id'], 'dQw4w9WgXcQ')
