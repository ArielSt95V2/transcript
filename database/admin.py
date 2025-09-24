from django.contrib import admin
from .models import Topic, InformationSource, UserQuestion, KnowledgeNode

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'knowledge_nodes_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    def knowledge_nodes_count(self, obj):
        """Show how many knowledge nodes are linked to this topic"""
        return obj.knowledgenode_set.count()
    knowledge_nodes_count.short_description = "Knowledge Nodes"

@admin.register(InformationSource)
class InformationSourceAdmin(admin.ModelAdmin):
    list_display = ['source_type', 'source_identifier', 'content_length', 'raw_content_preview', 'created_at', 'updated_at']
    list_filter = ['source_type', 'created_at', 'updated_at']
    search_fields = ['source_identifier', 'source_type']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_length(self, obj):
        """Show the length of raw content to quickly assess data size"""
        if obj.raw_content:
            return f"{len(obj.raw_content)} chars"
        return "No content"
    content_length.short_description = "Content Size"

    def raw_content_preview(self, obj):
        """Show first 100 characters of raw content"""
        if obj.raw_content:
            return obj.raw_content[:100] + "..." if len(obj.raw_content) > 100 else obj.raw_content
        return "No content"
    raw_content_preview.short_description = "Raw Content Preview"

@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'has_answer', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['question_text', 'answer_text', 'feedback']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_answer(self, obj):
        """Quick visual indicator if question has been answered"""
        return "✓" if obj.answer_text else "✗"
    has_answer.short_description = "Answered"

@admin.register(KnowledgeNode)
class KnowledgeNodeAdmin(admin.ModelAdmin):
    list_display = ['concept_name', 'topic', 'content_source', 'related_count', 'created_at']
    list_filter = ['topic', 'content_source__source_type', 'created_at']
    search_fields = ['concept_name', 'topic__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['related_nodes']  # Better UI for many-to-many relationships
    
    def related_count(self, obj):
        """Show how many other nodes are related to this one"""
        return obj.related_nodes.count()
    related_count.short_description = "Related Nodes"
