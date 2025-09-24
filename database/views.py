from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from .models import Topic, InformationSource, UserQuestion, KnowledgeNode
from .serializers import (
    TopicListSerializer, TopicDetailSerializer, TopicCreateUpdateSerializer,
    InformationSourceListSerializer, InformationSourceDetailSerializer, InformationSourceCreateUpdateSerializer,
    UserQuestionListSerializer, UserQuestionDetailSerializer, UserQuestionCreateUpdateSerializer,
    KnowledgeNodeListSerializer, KnowledgeNodeDetailSerializer, KnowledgeNodeCreateUpdateSerializer
)
from .utils import get_youtube_transcript
import re

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/topics/1/ and /api/topics/machine-learning/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Topic.objects.get(name=lookup_value)
        except Topic.DoesNotExist:
            raise Http404("No Topic matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TopicListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TopicCreateUpdateSerializer
        return TopicDetailSerializer

class InformationSourceViewSet(viewsets.ModelViewSet):
    queryset = InformationSource.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by source_identifier instead of just ID
        Supports both: /api/information-sources/1/ and /api/information-sources/dQw4w9WgXcQ/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by source_identifier
        try:
            return InformationSource.objects.get(source_identifier=lookup_value)
        except InformationSource.DoesNotExist:
            raise Http404("No InformationSource matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InformationSourceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return InformationSourceCreateUpdateSerializer
        return InformationSourceDetailSerializer

class UserQuestionViewSet(viewsets.ModelViewSet):
    queryset = UserQuestion.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by question_text (first 50 chars) instead of just ID
        Supports both: /api/user-questions/1/ and /api/user-questions/what-is-machine-learning/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by question_text (case-insensitive, partial match)
        try:
            # Convert URL-friendly format back to question text
            question_text = lookup_value.replace('-', ' ').title()
            return UserQuestion.objects.get(question_text__icontains=question_text)
        except UserQuestion.DoesNotExist:
            raise Http404("No UserQuestion matches the given query.")
        except UserQuestion.MultipleObjectsReturned:
            # If multiple matches, get the first one
            question_text = lookup_value.replace('-', ' ').title()
            return UserQuestion.objects.filter(question_text__icontains=question_text).first()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserQuestionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return UserQuestionCreateUpdateSerializer
        return UserQuestionDetailSerializer

class KnowledgeNodeViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeNode.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by concept_name instead of just ID
        Supports both: /api/knowledge-nodes/1/ and /api/knowledge-nodes/neural-networks/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by concept_name
        try:
            # Convert URL-friendly format back to concept name
            concept_name = lookup_value.replace('-', ' ').title()
            return KnowledgeNode.objects.get(concept_name__iexact=concept_name)
        except KnowledgeNode.DoesNotExist:
            raise Http404("No KnowledgeNode matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return KnowledgeNodeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return KnowledgeNodeCreateUpdateSerializer
        return KnowledgeNodeDetailSerializer


class TranscriptExtractView(APIView):
    """
    Dedicated view for extracting YouTube transcripts and automatically saving to InformationSource
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Extract transcript from a YouTube video URL and automatically save to InformationSource
        """
        video_url = request.data.get('video_url')
        
        if not video_url:
            return Response(
                {'error': 'video_url is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract video ID from URL for source_identifier
        match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", video_url)
        if not match:
            return Response(
                {'error': 'Invalid YouTube URL format.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        video_id = match.group(1)
        
        transcript = get_youtube_transcript(video_url)
        
        if transcript.startswith("Invalid") or transcript.startswith("Error"):
            return Response(
                {'error': transcript}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Automatically save to InformationSource model
        info_source = InformationSource.objects.create(
            source_type='youtube',
            source_identifier=video_id,
            raw_content=transcript
        )
        
        return Response({
            'transcript': transcript,
            'video_url': video_url,
            'video_id': video_id,
            'saved_id': info_source.id,
            'message': 'Transcript extracted and saved successfully'
        })
