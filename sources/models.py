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
