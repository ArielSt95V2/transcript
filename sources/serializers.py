from rest_framework import serializers
from .models import YouTubeTranscript
from database.serializers import BaseModelSerializer
import re

class YouTubeTranscriptListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    character_count = serializers.SerializerMethodField()
    
    class Meta:
        model = YouTubeTranscript
        fields = [
            'id', 'name', 'description', 'video_url', 'video_id', 
            'title', 'channel_name', 'language', 'status', 'status_display',
            'character_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_character_count(self, obj):
        """Return character count of transcript text"""
        return len(obj.transcript_text) if obj.transcript_text else 0


class YouTubeTranscriptDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    character_count = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()
    
    class Meta:
        model = YouTubeTranscript
        fields = [
            'id', 'name', 'description', 'video_url', 'video_id',
            'title', 'channel_name', 'transcript_text', 'language',
            'duration', 'status', 'status_display', 'error_message',
            'character_count', 'word_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_character_count(self, obj):
        """Return character count of transcript text"""
        return len(obj.transcript_text) if obj.transcript_text else 0
    
    def get_word_count(self, obj):
        """Return word count of transcript text"""
        if obj.transcript_text:
            return len(obj.transcript_text.split())
        return 0


class YouTubeTranscriptCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating YouTube transcripts"""
    
    class Meta:
        model = YouTubeTranscript
        fields = [
            'id', 'name', 'description', 'video_url', 'video_id',
            'title', 'channel_name', 'language', 'status'
        ]
        read_only_fields = ['id', 'video_id', 'status']
    
    def validate_name(self, value):
        """Validate name length"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()
    
    def validate_video_url(self, value):
        """Validate YouTube URL format and extract video ID"""
        youtube_pattern = r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})"
        match = re.search(youtube_pattern, value)
        
        if not match:
            raise serializers.ValidationError(
                "Invalid YouTube URL format. Please provide a valid YouTube video URL."
            )
        
        return value
    
    def validate(self, data):
        """Cross-field validation and auto-extract video_id"""
        video_url = data.get('video_url')
        
        if video_url:
            # Extract video ID from URL
            youtube_pattern = r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})"
            match = re.search(youtube_pattern, video_url)
            
            if match:
                video_id = match.group(1)
                
                # Check for duplicate video_id on create
                if not self.instance:
                    if YouTubeTranscript.objects.filter(video_id=video_id).exists():
                        existing = YouTubeTranscript.objects.get(video_id=video_id)
                        raise serializers.ValidationError({
                            'video_url': f"A transcript for this video already exists (ID: {existing.id}, Name: '{existing.name}').",
                            'video_id': video_id,
                            'existing_transcript_id': existing.id
                        })
                
                # Store video_id in validated data (will be set during create)
                data['video_id'] = video_id
        
        return data
    
    def create(self, validated_data):
        """Create transcript and trigger extraction"""
        from .transcript import extract_youtube_transcript
        
        # Extract video_id from validated data
        video_id = validated_data.get('video_id')
        video_url = validated_data.get('video_url')
        
        # Extract transcript BEFORE creating the record
        try:
            result = extract_youtube_transcript(video_url)
            
            if result.get('success'):
                # Set the actual transcript text and success status
                validated_data['transcript_text'] = result.get('transcript_text', '')
                validated_data['status'] = 'success'
                validated_data['error_message'] = None
                
                # Create instance with the actual transcript
                instance = super().create(validated_data)
                return instance
            else:
                # Extraction failed - DON'T create record, raise error
                error_msg = result.get('error', 'Unknown error occurred')
                raise serializers.ValidationError({
                    'video_url': f'Failed to extract transcript: {error_msg}'
                })
                
        except serializers.ValidationError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Unexpected exception during extraction
            raise serializers.ValidationError({
                'video_url': f'Error extracting transcript: {str(e)}'
            })