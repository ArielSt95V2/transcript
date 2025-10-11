from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
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
from .utils.llm_analyze import LLMAnalyzer
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
    
    def handle_exception(self, exc):
        """
        Standardize error responses for frontend compatibility.
        Returns consistent error format: {error, field_errors, error_code, meta}
        """
        response_data = {}
        status_code = status.HTTP_400_BAD_REQUEST
        
        # 1. Handle DRF ValidationError
        if isinstance(exc, ValidationError):
            if isinstance(exc.detail, dict):
                # Field-specific errors - exclude metadata fields
                field_errors = {}
                meta = {}
                
                for field, error in exc.detail.items():
                    # Check if this is metadata (not a form field)
                    if field in ['existing_transcript_id', 'existing_content_id']:
                        meta[field] = error[0] if isinstance(error, list) else error
                    else:
                        # Regular field error
                        if isinstance(error, list):
                            field_errors[field] = error[0]
                        else:
                            field_errors[field] = str(error)
                
                response_data = {
                    "error": "Validation failed. Please check the form fields.",
                    "field_errors": field_errors,
                    "error_code": "VALIDATION_ERROR"
                }
                
                # Add metadata if present
                if meta:
                    response_data["meta"] = meta
            else:
                # General validation error
                error_msg = exc.detail[0] if isinstance(exc.detail, list) else str(exc.detail)
                response_data = {
                    "error": error_msg,
                    "error_code": "VALIDATION_ERROR"
                }
        
        # 2. Handle 404 errors
        elif isinstance(exc, (ObjectDoesNotExist, Http404)):
            model_name = self.queryset.model.__name__ if hasattr(self, 'queryset') else "Resource"
            response_data = {
                "error": f"{model_name} not found",
                "error_code": "NOT_FOUND"
            }
            status_code = status.HTTP_404_NOT_FOUND
        
        # 3. Handle permission errors
        elif isinstance(exc, PermissionDenied):
            response_data = {
                "error": "You do not have permission to perform this action",
                "error_code": "PERMISSION_DENIED"
            }
            status_code = status.HTTP_403_FORBIDDEN
        
        # 4. Handle all other errors
        else:
            # Let DRF handle, then reformat
            response = super().handle_exception(exc)
            
            if hasattr(response, 'data'):
                if isinstance(response.data, dict):
                    if 'detail' in response.data:
                        response_data = {
                            "error": str(response.data['detail']),
                            "error_code": "SERVER_ERROR"
                        }
                    else:
                        # Unknown dict format - treat as field errors
                        response_data = {
                            "error": "An error occurred",
                            "field_errors": response.data,
                            "error_code": "UNKNOWN_ERROR"
                        }
                else:
                    response_data = {
                        "error": str(response.data),
                        "error_code": "SERVER_ERROR"
                    }
            
            return Response(response_data, status=response.status_code)
        
        return Response(response_data, status=status_code)


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


class ChatbotAssistView(APIView):
    """
    API endpoint for chatbot assistance.
    Helps users fill form fields using AI conversation.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handle chatbot assistance requests.
        
        Expected payload:
        {
            "message": "user message",
            "entity_type": "Component|Concept|Reference|Technique|Theme|Tool|Composition",
            "field_name": "description|instructions|outcome|name|etc",
            "form_data": {...},
            "conversation_history": [{"role": "user|assistant", "content": "..."}]
        }
        """
        try:
            # Extract request data
            user_message = request.data.get('message', '')
            entity_type = request.data.get('entity_type', '')
            field_name = request.data.get('field_name')
            form_data = request.data.get('form_data', {})
            conversation_history = request.data.get('conversation_history', [])
            
            # Validate required fields
            if not user_message:
                return Response(
                    {'error': 'Message is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not entity_type:
                return Response(
                    {'error': 'Entity type is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize LLM analyzer
            analyzer = LLMAnalyzer()
            
            # Get AI response
            result = analyzer.chat_assist(
                user_message=user_message,
                entity_type=entity_type,
                field_name=field_name,
                form_data=form_data,
                conversation_history=conversation_history
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )