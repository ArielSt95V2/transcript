from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, InformationSourceViewSet, UserQuestionViewSet, KnowledgeNodeViewSet, TranscriptExtractView

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'information-sources', InformationSourceViewSet)
router.register(r'user-questions', UserQuestionViewSet)
router.register(r'knowledge-nodes', KnowledgeNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('extract-transcript/', TranscriptExtractView.as_view(), name='extract-transcript'),
]
