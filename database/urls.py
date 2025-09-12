from django.urls import path
from .views import YouTubeTranscriptIngestView, ProfessionListView, youtube_transcript_ui, download_transcript, TranscriptListView

urlpatterns = [
    path('content/ingest-youtube/', YouTubeTranscriptIngestView.as_view(), name='content-ingest-youtube'),
    path('professions/', ProfessionListView.as_view(), name='profession-list'),
    path('transcripts/', TranscriptListView.as_view(), name='transcript-list'),
    path('youtube-ui/', youtube_transcript_ui, name='youtube-transcript-ui'),
    path('download-transcript/<int:content_id>/', download_transcript, name='download-transcript'),
]


