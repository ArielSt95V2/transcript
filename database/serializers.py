# serializers.py
# In Django REST Framework, you need serializers to convert between Python objects and JSON for your API

from rest_framework import serializers
from .models import Topic, InformationSource, UserQuestion, KnowledgeNode

# Base serializer with common fields
class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer that all other serializers can inherit from"""
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        abstract = True

# Topic Serializers
class TopicListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    knowledge_nodes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'knowledge_nodes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_knowledge_nodes_count(self, obj):
        return obj.knowledgenode_set.count()

class TopicDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views with related data"""
    knowledge_nodes = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'knowledge_nodes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_knowledge_nodes(self, obj):
        nodes = obj.knowledgenode_set.all()[:10]  # Limit to avoid large payloads
        return KnowledgeNodeListSerializer(nodes, many=True, context=self.context).data

class TopicCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating topics"""
    class Meta:
        model = Topic
        fields = ['name', 'description']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Topic name must be at least 2 characters long")
        return value.strip()

# InformationSource Serializers
class InformationSourceListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)
    knowledge_nodes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InformationSource
        fields = ['id', 'source_type', 'source_type_display', 'source_identifier', 
                 'knowledge_nodes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_knowledge_nodes_count(self, obj):
        return obj.knowledgenode_set.count()

class InformationSourceDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)
    knowledge_nodes = serializers.SerializerMethodField()
    
    class Meta:
        model = InformationSource
        fields = ['id', 'source_type', 'source_type_display', 'source_identifier', 
                 'raw_content', 'processed_content', 'knowledge_nodes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_knowledge_nodes(self, obj):
        nodes = obj.knowledgenode_set.all()[:20]  # Limit to avoid large payloads
        return KnowledgeNodeListSerializer(nodes, many=True, context=self.context).data

class InformationSourceCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating information sources"""
    class Meta:
        model = InformationSource
        fields = ['source_type', 'source_identifier', 'raw_content', 'processed_content']
    
    def validate_source_identifier(self, value):
        if not value.strip():
            raise serializers.ValidationError("Source identifier cannot be empty")
        return value.strip()
    
    def validate_source_type(self, value):
        valid_types = [choice[0] for choice in InformationSource.SOURCE_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid source type. Must be one of: {', '.join(valid_types)}")
        return value

# UserQuestion Serializers
class UserQuestionListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    has_answer = serializers.SerializerMethodField()
    
    class Meta:
        model = UserQuestion
        fields = ['id', 'question_text', 'has_answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_has_answer(self, obj):
        return bool(obj.answer_text)

class UserQuestionDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    class Meta:
        model = UserQuestion
        fields = ['id', 'question_text', 'answer_text', 'feedback', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserQuestionCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating user questions"""
    class Meta:
        model = UserQuestion
        fields = ['question_text', 'answer_text', 'feedback']
    
    def validate_question_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Question must be at least 10 characters long")
        return value.strip()

# KnowledgeNode Serializers
class KnowledgeNodeListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    content_source_type = serializers.CharField(source='content_source.source_type', read_only=True)
    related_nodes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeNode
        fields = ['id', 'concept_name', 'topic_name', 'content_source_type', 
                 'related_nodes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_related_nodes_count(self, obj):
        return obj.related_nodes.count()

class KnowledgeNodeDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views with nested relationships"""
    topic = TopicListSerializer(read_only=True)
    content_source = InformationSourceListSerializer(read_only=True)
    related_nodes = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeNode
        fields = ['id', 'concept_name', 'topic', 'content_source', 'related_nodes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_related_nodes(self, obj):
        related = obj.related_nodes.all()[:10]  # Limit to avoid large payloads
        return KnowledgeNodeListSerializer(related, many=True, context=self.context).data

class KnowledgeNodeCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating knowledge nodes"""
    class Meta:
        model = KnowledgeNode
        fields = ['topic', 'content_source', 'concept_name', 'related_nodes']
    
    def validate_concept_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Concept name must be at least 2 characters long")
        return value.strip()
    
    def validate(self, data):
        # Ensure topic and content_source exist
        if 'topic' in data and not data['topic']:
            raise serializers.ValidationError("Topic is required")
        if 'content_source' in data and not data['content_source']:
            raise serializers.ValidationError("Content source is required")
        return data

# Mobile-optimized serializers (smaller payloads)
class MobileKnowledgeNodeSerializer(BaseModelSerializer):
    """Ultra-lightweight serializer for mobile apps"""
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    
    class Meta:
        model = KnowledgeNode
        fields = ['id', 'concept_name', 'topic_name', 'created_at']
        read_only_fields = ['id', 'created_at']

# Search/Filter serializers
class KnowledgeNodeSearchSerializer(BaseModelSerializer):
    """Serializer optimized for search results"""
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    content_source_identifier = serializers.CharField(source='content_source.source_identifier', read_only=True)
    
    class Meta:
        model = KnowledgeNode
        fields = ['id', 'concept_name', 'topic_name', 'content_source_identifier', 'created_at']

