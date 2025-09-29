from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DomainViewSet, SubDomainViewSet, PhaseViewSet, ConceptViewSet, ThemeViewSet,
    ReferenceViewSet, ComponentViewSet, ToolViewSet, TechniqueViewSet, CompositionViewSet,
    TranscriptExtractView, CompositionBuilderView, composition_builder_view,
    DataManagerView, BulkImportView, DataExportView, EntityListView, EntityDetailView, data_manager_view
)

router = DefaultRouter()
router.register(r'domains', DomainViewSet)
router.register(r'subdomains', SubDomainViewSet)
router.register(r'phases', PhaseViewSet)
router.register(r'concepts', ConceptViewSet)
router.register(r'themes', ThemeViewSet)
router.register(r'references', ReferenceViewSet)
router.register(r'components', ComponentViewSet)
router.register(r'tools', ToolViewSet)
router.register(r'techniques', TechniqueViewSet)
router.register(r'compositions', CompositionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('extract-transcript/', TranscriptExtractView.as_view(), name='extract-transcript'),
    path('composition-builder/', CompositionBuilderView.as_view(), name='composition-builder'),
    path('composition-builder-ui/', composition_builder_view, name='composition-builder-ui'),
    
    # Data Management Endpoints
    path('data-manager/', DataManagerView.as_view(), name='data-manager'),
    path('data-manager/import/', BulkImportView.as_view(), name='bulk-import'),
    path('data-manager/export/', DataExportView.as_view(), name='data-export'),
    path('data-manager/entities/<str:entity_type>/', EntityListView.as_view(), name='entity-list'),
    path('data-manager/entity/<str:entity_type>/<int:entity_id>/', EntityDetailView.as_view(), name='entity-detail'),
    path('data-manager-ui/', data_manager_view, name='data-manager-ui'),
]