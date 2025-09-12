# serializers.py
# In Django REST Framework, you need serializers to convert between Python objects and JSON for your API


from rest_framework import serializers
from .models import Conversation, Message, MessageFeedback

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user_id', 'title', 'created_at', 'updated_at', 'messages',
'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

class MessageFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFeedback
        fields = ['id', 'message', 'feedback_type', 'feedback_text', 'created_at']
        read_only_fields = ['id', 'created_at']

# For creating new messages in conversations
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'role', 'content']



from .models import Profession, ContentSource, ContentMetadata
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import exceptions
import os

class ContentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentMetadata
        fields = ['id', 'metadata_key', 'metadata_value', 'created_at']
        read_only_fields = ['id', 'created_at']

class ContentSourceSerializer(serializers.ModelSerializer):
    metadata = ContentMetadataSerializer(many=True, read_only=True)
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)
    # TRACE: This field will be computed by get_content_preview() method below
    content_preview = serializers.SerializerMethodField()

    class Meta:
        model = ContentSource
        fields = [
            'id', 'profession', 'source_type', 'source_type_display',
            'title', 'content', 'content_preview', 'source_url',  # TRACE: content_preview included in API response
            'created_at', 'updated_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_content_preview(self, obj):
        """
        TRACE: This method is called by DRF when serializing ContentSource objects
        - obj = ContentSource instance (e.g., with full transcript text)
        - Returns: First 200 chars + "..." if longer, or full content if shorter
        - Used in: API response as 'content_preview' field
        - Displayed in: UI success view as result.content_preview
        """
        return obj.content[:200] + "..." if len(obj.content) > 200 else obj.content






class ContentSourceCreateSerializer(serializers.ModelSerializer):
    metadata = serializers.DictField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = ContentSource
        fields = ['profession', 'source_type', 'title', 'content', 'source_url', 'metadata']

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata', {})
        content_source = ContentSource.objects.create(**validated_data)

        # Create metadata entries
        for key, value in metadata_data.items():
            ContentMetadata.objects.create(
                content_source=content_source,
                metadata_key=key,
                metadata_value=value
            )

        return content_source






class ProfessionSerializer(serializers.ModelSerializer):
    content_count = serializers.SerializerMethodField()
    source_type_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = Profession
        fields = ['id', 'name', 'description', 'created_at', 'content_count', 'source_type_breakdown']
        read_only_fields = ['id', 'created_at']

    def get_content_count(self, obj):
        return obj.content_sources.count()

    def get_source_type_breakdown(self, obj):
        from django.db.models import Count
        return dict(
            obj.content_sources.values('source_type').annotate(count=Count('source_type')).values_list('source_type', 'count')
        )

class ProfessionDetailSerializer(serializers.ModelSerializer):
    content_sources = ContentSourceSerializer(many=True, read_only=True)
    content_count = serializers.SerializerMethodField()

    class Meta:
        model = Profession
        fields = ['id', 'name', 'description', 'created_at', 'content_count', 'content_sources']
        read_only_fields = ['id', 'created_at']

    def get_content_count(self, obj):
        return obj.content_sources.count()