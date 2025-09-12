from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.db import transaction
import re
import os
from django.conf import settings
from .serializers import ContentSourceCreateSerializer, ContentSourceSerializer, ProfessionSerializer
from .models import Profession, ContentMetadata, ContentSource




def get_youtube_transcript(video_url):
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter

    # Extract video ID from various YouTube URL formats
    match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", video_url)
    if not match:
        return "Invalid YouTube URL format."
    video_id = match.group(1)

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=['en'])
        
        # Format the transcript as plain text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)

        return formatted_transcript

    except Exception as e:
        return str(e)

class YouTubeTranscriptIngestView(APIView):
    def post(self, request, *args, **kwargs):
        video_url = request.data.get('video_url')
        profession_id = request.data.get('profession')
        title = request.data.get('title') or 'YouTube Transcript'
        metadata = request.data.get('metadata', {})  # optional dict

        if not video_url or not profession_id:
            return Response({'detail': 'video_url and profession are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate profession exists first
        try:
            profession = Profession.objects.get(pk=profession_id)
        except Profession.DoesNotExist:
            return Response({'detail': 'Profession not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get transcript with error handling
        try:
            transcript_text = get_youtube_transcript(video_url)
            if not transcript_text or transcript_text.startswith('Invalid YouTube URL'):
                return Response({'detail': transcript_text or 'Failed to fetch transcript'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error fetching transcript: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Only save to database if everything is successful
        try:
            with transaction.atomic():
                data = {
                    'profession': profession_id,
                    'source_type': 'youtube_transcript',
                    'title': title,
                    'content': transcript_text,
                    'source_url': video_url,
                    'metadata': metadata,
                }

                serializer = ContentSourceCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                content_source = serializer.save()
                
                # Create .txt file with transcript content
                self._create_transcript_file(content_source, transcript_text)
                
                # TRACE: ContentSourceSerializer converts ContentSource object to JSON
                # - Calls get_content_preview() method to compute content_preview field
                # - Returns JSON with all fields including content_preview
                # - This JSON becomes the API response sent to frontend
                return Response(ContentSourceSerializer(content_source).data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'detail': f'Error saving data: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _create_transcript_file(self, content_source, transcript_text):
        """Create a .txt file with the transcript content"""
        try:
            # Create transcripts directory if it doesn't exist
            transcripts_dir = os.path.join(settings.MEDIA_ROOT, 'transcripts')
            os.makedirs(transcripts_dir, exist_ok=True)
            
            # Create filename with content source ID and title
            safe_title = "".join(c for c in content_source.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"transcript_{content_source.id}_{safe_title}.txt"
            file_path = os.path.join(transcripts_dir, filename)
            
            # Write transcript to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {content_source.title}\n")
                f.write(f"Source URL: {content_source.source_url}\n")
                f.write(f"Profession: {content_source.profession.name}\n")
                f.write(f"Created: {content_source.created_at}\n")
                f.write("-" * 50 + "\n\n")
                f.write(transcript_text)
                
            # Store file path in metadata
            ContentMetadata.objects.create(
                content_source=content_source,
                metadata_key='transcript_file',
                metadata_value=file_path
            )
            
        except Exception as e:
            # Log error but don't fail the main operation
            print(f"Warning: Could not create transcript file: {str(e)}")

class ProfessionListView(APIView):
    def get(self, request, *args, **kwargs):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True)
        return Response(serializer.data)

def youtube_transcript_ui(request):
    return render(request, 'youtube_transcript.html')

class TranscriptListView(ListAPIView):
    """
    TRACE: List all YouTube transcripts with filtering, search, and pagination
    - GET /api/transcripts/ - List all transcripts
    - GET /api/transcripts/?search=python - Search in titles
    - GET /api/transcripts/?profession=1 - Filter by profession
    - GET /api/transcripts/?ordering=-created_at - Sort by newest first
    """
    serializer_class = ContentSourceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']  # Search in title and content
    filterset_fields = ['profession']  # Filter by profession ID
    ordering_fields = ['created_at', 'title', 'profession']  # Sortable fields
    ordering = ['-created_at']  # Default: newest first
    
    def get_queryset(self):
        """
        TRACE: Filter only YouTube transcripts from ContentSource
        - Returns: QuerySet of ContentSource objects with source_type='youtube_transcript'
        - Used by: ListAPIView to display paginated results
        """
        return ContentSource.objects.filter(source_type='youtube_transcript').select_related('profession').prefetch_related('metadata')

def download_transcript(request, content_id):
    """Download the transcript file for a specific content source"""
    try:
        content_source = ContentSource.objects.get(id=content_id)
        transcript_metadata = content_source.metadata.filter(metadata_key='transcript_file').first()
        
        if not transcript_metadata:
            return HttpResponse("Transcript file not found", status=404)
            
        file_path = transcript_metadata.metadata_value
        
        if not os.path.exists(file_path):
            return HttpResponse("Transcript file not found on disk", status=404)
            
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="transcript_{content_id}_{content_source.title}.txt"'
            return response
            
    except ContentSource.DoesNotExist:
        return HttpResponse("Content not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)