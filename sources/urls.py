from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YouTubeTranscriptViewSet

router = DefaultRouter()
router.register(r'youtube-transcripts', YouTubeTranscriptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

