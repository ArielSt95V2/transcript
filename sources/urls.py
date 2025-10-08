from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YouTubeTranscriptViewSet, WebContentSourceViewSet

router = DefaultRouter()
router.register(r'youtube-transcripts', YouTubeTranscriptViewSet)
router.register(r'web-content', WebContentSourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

