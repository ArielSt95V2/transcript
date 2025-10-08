import logging
logger = logging.getLogger(__name__)


from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from database.views import BaseNamedModelViewSet
from .models import YouTubeTranscript
from .serializers import (
    YouTubeTranscriptListSerializer,
    YouTubeTranscriptDetailSerializer,
    YouTubeTranscriptCreateUpdateSerializer
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
        """Override create to provide better error handling"""
        try:
            serializer = self.get_serializer(data=request.data)
            
            # Validate the data
            if not serializer.is_valid():
                logger.error(f"Validation errors: {serializer.errors}")
                return Response(
                    {
                        'error': 'Validation failed',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the instance
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
            
        except Exception as e:
            logger.error(f"Error creating YouTube transcript: {str(e)}")
            return Response(
                {
                    'error': 'Failed to create transcript',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    
