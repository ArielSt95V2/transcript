from django.db import models
from database.models import BaseModel

class YouTubeTranscript(BaseModel):
    """
    Model to store YouTube video transcripts with metadata.
    Supports extraction status tracking and error handling.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    video_url = models.URLField(max_length=500)
    video_id = models.CharField(max_length=20, unique=True, db_index=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    transcript_text = models.TextField()
    language = models.CharField(max_length=10, default='en')
    duration = models.DurationField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.video_id} ({self.status})"
    
    class Meta:
        verbose_name = "YouTube Transcript"
        verbose_name_plural = "YouTube Transcripts"
        ordering = ['-created_at']


class WebContentSource(BaseModel):
    """
    Model to store web content extracted via Firecrawl API.
    Supports markdown, HTML, and structured JSON extraction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    source_url = models.URLField(max_length=1000, unique=True, db_index=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    content_markdown = models.TextField()
    content_html = models.TextField(blank=True, null=True)
    extracted_json = models.JSONField(blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.source_url[:50]} ({self.status})"
    
    class Meta:
        verbose_name = "Web Content Source"
        verbose_name_plural = "Web Content Sources"
        ordering = ['-created_at']