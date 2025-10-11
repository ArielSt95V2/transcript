import logging
logger = logging.getLogger(__name__)


from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from database.views import BaseNamedModelViewSet
from .models import YouTubeTranscript, WebContentSource
from .serializers import (
    YouTubeTranscriptListSerializer,
    YouTubeTranscriptDetailSerializer,
    YouTubeTranscriptCreateUpdateSerializer,
    WebContentSourceListSerializer,
    WebContentSourceDetailSerializer,
    WebContentSourceCreateUpdateSerializer
)
from .transcript import extract_youtube_transcript


class YouTubeTranscriptViewSet(BaseNamedModelViewSet):
    """
    ViewSet for YouTube Transcript CRUD operations.
    Supports filtering by status and re-extraction of failed transcripts.
    """
    queryset = YouTubeTranscript.objects.all()
    list_serializer_class = YouTubeTranscriptListSerializer
    detail_serializer_class = YouTubeTranscriptDetailSerializer
    create_update_serializer_class = YouTubeTranscriptCreateUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to check for duplicates and handle errors"""
        video_url = request.data.get('video_url')
        
        # Check for duplicate video URL
        if video_url:
            existing = YouTubeTranscript.objects.filter(video_url=video_url).first()
            if existing:
                raise ValidationError({
                    "video_url": ["A transcript for this video already exists"],
                    "existing_transcript_id": [existing.id]
                })
        
        # Proceed with standard creation
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        """Filter queryset by query parameters"""
        queryset = super().get_queryset()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by language
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)
        
        # Search by video_id
        video_id = self.request.query_params.get('video_id')
        if video_id:
            queryset = queryset.filter(video_id=video_id)
        
        return queryset


class WebContentSourceViewSet(BaseNamedModelViewSet):
    """
    ViewSet for Web Content Source CRUD operations.
    Supports filtering by status and language.
    """
    queryset = WebContentSource.objects.all()
    list_serializer_class = WebContentSourceListSerializer
    detail_serializer_class = WebContentSourceDetailSerializer
    create_update_serializer_class = WebContentSourceCreateUpdateSerializer
    
    # Special Error Handling for Duplicates
    def create(self, request, *args, **kwargs):
        """Override create to check for duplicates and handle errors"""
        source_url = request.data.get('source_url')
        
        # Check for duplicate source URL
        if source_url:
            existing = WebContentSource.objects.filter(source_url=source_url).first()
            if existing:
                raise ValidationError({
                    "source_url": ["Content from this URL already exists"],
                    "existing_content_id": [existing.id]
                })
        
        # Proceed with standard creation
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        """Filter queryset by query parameters"""
        queryset = super().get_queryset()
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Filter by language
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)
        
        # Filter by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        
        return queryset
    
