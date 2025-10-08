from django.contrib import admin
from .models import YouTubeTranscript


@admin.register(YouTubeTranscript)
class YouTubeTranscriptAdmin(admin.ModelAdmin):
    """Admin interface for YouTube Transcript model"""
    
    list_display = ['video_id', 'name', 'status', 'language', 'created_at']
    list_filter = ['status', 'language', 'created_at']
    search_fields = ['name', 'video_url', 'video_id', 'title', 'channel_name']
    readonly_fields = ['video_id', 'status', 'created_at', 'updated_at', 'error_message']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Video Information', {
            'fields': ('video_url', 'video_id', 'title', 'channel_name', 'language', 'duration')
        }),
        ('Transcript Data', {
            'fields': ('transcript_text', 'status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly when editing"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ['video_url']
        return self.readonly_fields
