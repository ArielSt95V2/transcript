from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
from django.shortcuts import render
from .models import Domain, SubDomain, Phase, Concept, Theme, Reference, Component, Tool, Technique, Composition
from .serializers import (
    DomainListSerializer, DomainDetailSerializer, DomainCreateUpdateSerializer,
    SubDomainListSerializer, SubDomainDetailSerializer, SubDomainCreateUpdateSerializer,
    PhaseListSerializer, PhaseDetailSerializer, PhaseCreateUpdateSerializer,
    ConceptListSerializer, ConceptDetailSerializer, ConceptCreateUpdateSerializer,
    ThemeListSerializer, ThemeDetailSerializer, ThemeCreateUpdateSerializer,
    ReferenceListSerializer, ReferenceDetailSerializer, ReferenceCreateUpdateSerializer,
    ComponentListSerializer, ComponentDetailSerializer, ComponentCreateUpdateSerializer,
    ToolListSerializer, ToolDetailSerializer, ToolCreateUpdateSerializer,
    TechniqueListSerializer, TechniqueDetailSerializer, TechniqueCreateUpdateSerializer,
    CompositionListSerializer, CompositionDetailSerializer, CompositionCreateUpdateSerializer
)
from .utils.transcript import get_youtube_transcript
import re

# Base ViewSet with common logic
class BaseNamedModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that supports lookup by name or ID and automatic serializer selection.
    
    Subclasses should define:
    - queryset
    - list_serializer_class
    - detail_serializer_class
    - create_update_serializer_class
    """
    permission_classes = [AllowAny]
    list_serializer_class = None
    detail_serializer_class = None
    create_update_serializer_class = None
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID.
        Supports both: /api/domains/1/ and /api/domains/filmmaking/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return self.queryset.model.objects.get(name=lookup_value)
        except self.queryset.model.DoesNotExist:
            model_name = self.queryset.model.__name__
            raise Http404(f"No {model_name} matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        elif self.action in ['create', 'update', 'partial_update']:
            return self.create_update_serializer_class
        return self.detail_serializer_class


# Now each ViewSet is just 5 lines
class DomainViewSet(BaseNamedModelViewSet):
    queryset = Domain.objects.all()
    list_serializer_class = DomainListSerializer
    detail_serializer_class = DomainDetailSerializer
    create_update_serializer_class = DomainCreateUpdateSerializer

class SubDomainViewSet(BaseNamedModelViewSet):
    queryset = SubDomain.objects.all()
    list_serializer_class = SubDomainListSerializer
    detail_serializer_class = SubDomainDetailSerializer
    create_update_serializer_class = SubDomainCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        domain_id = self.request.query_params.get('domain')
        if domain_id:
            queryset = queryset.filter(domain_id=domain_id)
        return queryset

class PhaseViewSet(BaseNamedModelViewSet):
    queryset = Phase.objects.all()
    list_serializer_class = PhaseListSerializer
    detail_serializer_class = PhaseDetailSerializer
    create_update_serializer_class = PhaseCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sub_domain_id = self.request.query_params.get('sub_domain')
        if sub_domain_id:
            queryset = queryset.filter(sub_domain_id=sub_domain_id)
        return queryset

class ConceptViewSet(BaseNamedModelViewSet):
    queryset = Concept.objects.all()
    list_serializer_class = ConceptListSerializer
    detail_serializer_class = ConceptDetailSerializer
    create_update_serializer_class = ConceptCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by domain
        domain_id = self.request.query_params.get('domain')
        if domain_id:
            queryset = queryset.filter(domain_id=domain_id)
        # Filter by sub_domain
        sub_domain_id = self.request.query_params.get('sub_domain')
        if sub_domain_id:
            queryset = queryset.filter(sub_domain_id=sub_domain_id)
        # Filter by phase
        phase_id = self.request.query_params.get('phase')
        if phase_id:
            queryset = queryset.filter(phase_id=phase_id)
        return queryset

class ThemeViewSet(BaseNamedModelViewSet):
    queryset = Theme.objects.all()
    list_serializer_class = ThemeListSerializer
    detail_serializer_class = ThemeDetailSerializer
    create_update_serializer_class = ThemeCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by concept
        concept_id = self.request.query_params.get('concept')
        if concept_id:
            queryset = queryset.filter(concept_id=concept_id)
        return queryset

class ReferenceViewSet(BaseNamedModelViewSet):
    queryset = Reference.objects.all()
    list_serializer_class = ReferenceListSerializer
    detail_serializer_class = ReferenceDetailSerializer
    create_update_serializer_class = ReferenceCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by sub_domain
        sub_domain_id = self.request.query_params.get('sub_domain')
        if sub_domain_id:
            queryset = queryset.filter(sub_domain_id=sub_domain_id)
        # Filter by reference_type
        ref_type = self.request.query_params.get('reference_type')
        if ref_type:
            queryset = queryset.filter(reference_type=ref_type)
        return queryset

class ComponentViewSet(BaseNamedModelViewSet):
    queryset = Component.objects.all()
    list_serializer_class = ComponentListSerializer
    detail_serializer_class = ComponentDetailSerializer
    create_update_serializer_class = ComponentCreateUpdateSerializer

class ToolViewSet(BaseNamedModelViewSet):
    queryset = Tool.objects.all()
    list_serializer_class = ToolListSerializer
    detail_serializer_class = ToolDetailSerializer
    create_update_serializer_class = ToolCreateUpdateSerializer

class TechniqueViewSet(BaseNamedModelViewSet):
    queryset = Technique.objects.all()
    list_serializer_class = TechniqueListSerializer
    detail_serializer_class = TechniqueDetailSerializer
    create_update_serializer_class = TechniqueCreateUpdateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by phase
        phase_id = self.request.query_params.get('phase')
        if phase_id:
            queryset = queryset.filter(phase_id=phase_id)
        # Filter by theme (M2M)
        theme_id = self.request.query_params.get('theme')
        if theme_id:
            queryset = queryset.filter(themes__id=theme_id)
        return queryset
        
class CompositionViewSet(BaseNamedModelViewSet):
    queryset = Composition.objects.all()
    list_serializer_class = CompositionListSerializer
    detail_serializer_class = CompositionDetailSerializer
    create_update_serializer_class = CompositionCreateUpdateSerializer