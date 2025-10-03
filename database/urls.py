from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DomainViewSet, SubDomainViewSet, PhaseViewSet, ConceptViewSet, ThemeViewSet,
    ReferenceViewSet, ComponentViewSet, ToolViewSet, TechniqueViewSet, CompositionViewSet
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

]