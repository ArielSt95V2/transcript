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

# Domain ViewSet
class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/domains/1/ and /api/domains/filmmaking/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Domain.objects.get(name=lookup_value)
        except Domain.DoesNotExist:
            raise Http404("No Domain matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DomainListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DomainCreateUpdateSerializer
        return DomainDetailSerializer

# SubDomain ViewSet
class SubDomainViewSet(viewsets.ModelViewSet):
    queryset = SubDomain.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/subdomains/1/ and /api/subdomains/post-production/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return SubDomain.objects.get(name=lookup_value)
        except SubDomain.DoesNotExist:
            raise Http404("No SubDomain matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SubDomainListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SubDomainCreateUpdateSerializer
        return SubDomainDetailSerializer

# Phase ViewSet
class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/phases/1/ and /api/phases/video-editing/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Phase.objects.get(name=lookup_value)
        except Phase.DoesNotExist:
            raise Http404("No Phase matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PhaseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PhaseCreateUpdateSerializer
        return PhaseDetailSerializer

# Concept ViewSet
class ConceptViewSet(viewsets.ModelViewSet):
    queryset = Concept.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/concepts/1/ and /api/concepts/movie-trailer/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Concept.objects.get(name=lookup_value)
        except Concept.DoesNotExist:
            raise Http404("No Concept matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ConceptListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ConceptCreateUpdateSerializer
        return ConceptDetailSerializer

# Theme ViewSet
class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/themes/1/ and /api/themes/exciting-and-emotional/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Theme.objects.get(name=lookup_value)
        except Theme.DoesNotExist:
            raise Http404("No Theme matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ThemeListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ThemeCreateUpdateSerializer
        return ThemeDetailSerializer

# Reference ViewSet
class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/references/1/ and /api/references/reference-1/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Reference.objects.get(name=lookup_value)
        except Reference.DoesNotExist:
            raise Http404("No Reference matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ReferenceListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ReferenceCreateUpdateSerializer
        return ReferenceDetailSerializer

# Component ViewSet
class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/components/1/ and /api/components/music-cue-1/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Component.objects.get(name=lookup_value)
        except Component.DoesNotExist:
            raise Http404("No Component matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ComponentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ComponentCreateUpdateSerializer
        return ComponentDetailSerializer

# Tool ViewSet
class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/tools/1/ and /api/tools/marker-tool/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Tool.objects.get(name=lookup_value)
        except Tool.DoesNotExist:
            raise Http404("No Tool matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ToolListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ToolCreateUpdateSerializer
        return ToolDetailSerializer

# Technique ViewSet
class TechniqueViewSet(viewsets.ModelViewSet):
    queryset = Technique.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/techniques/1/ and /api/techniques/cutting-to-the-beat/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Technique.objects.get(name=lookup_value)
        except Technique.DoesNotExist:
            raise Http404("No Technique matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TechniqueListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TechniqueCreateUpdateSerializer
        return TechniqueDetailSerializer

# Composition ViewSet
class CompositionViewSet(viewsets.ModelViewSet):
    queryset = Composition.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        """
        Override to allow lookup by name instead of just ID
        Supports both: /api/compositions/1/ and /api/compositions/action-trailer-edit/
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (for backward compatibility)
        if lookup_value.isdigit():
            return super().get_object()
        
        # If not a digit, try to get by name
        try:
            return Composition.objects.get(name=lookup_value)
        except Composition.DoesNotExist:
            raise Http404("No Composition matches the given query.")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompositionListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CompositionCreateUpdateSerializer
        return CompositionDetailSerializer

# Custom API Views
class TranscriptExtractView(APIView):
    """
    Dedicated view for extracting YouTube transcripts and automatically saving to Reference
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Extract transcript from a YouTube video URL and automatically save to Reference
        """
        video_url = request.data.get('video_url')
        
        if not video_url:
            return Response(
                {'error': 'video_url is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract video ID from URL for source_identifier
        match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", video_url)
        if not match:
            return Response(
                {'error': 'Invalid YouTube URL format.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        video_id = match.group(1)
        
        transcript = get_youtube_transcript(video_url)
        
        if transcript.startswith("Invalid") or transcript.startswith("Error"):
            return Response(
                {'error': transcript}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Automatically save to Reference model
        reference = Reference.objects.create(
            name=f"YouTube Video {video_id}",
            description=f"Transcript from YouTube video: {video_url}",
            reference_type='youtube',
            content_url=video_url
        )
        
        return Response({
            'transcript': transcript,
            'video_url': video_url,
            'video_id': video_id,
            'saved_id': reference.id,
            'message': 'Transcript extracted and saved successfully'
        })

class CompositionBuilderView(APIView):
    """
    Custom view for building compositions with hierarchical data
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get hierarchical data for composition builder
        """
        domains = Domain.objects.filter(is_active=True).prefetch_related(
            'sub_domains__phases__concepts__themes'
        )
        
        serializer = DomainDetailSerializer(domains, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a composition with all related data
        """
        data = request.data
        
        # Create composition
        composition_data = {
            'name': data.get('name'),
            'description': data.get('description'),
            'domain_id': data.get('domain_id'),
            'sub_domain_id': data.get('sub_domain_id'),
            'phase_id': data.get('phase_id'),
            'concept_id': data.get('concept_id'),
            'theme_id': data.get('theme_id'),
        }
        
        serializer = CompositionCreateUpdateSerializer(data=composition_data)
        if serializer.is_valid():
            composition = serializer.save()
            
            # Add related objects
            if data.get('technique_ids'):
                composition.techniques.set(data['technique_ids'])
            if data.get('tool_ids'):
                composition.tools.set(data['tool_ids'])
            if data.get('component_ids'):
                composition.components.set(data['component_ids'])
            if data.get('reference_ids'):
                composition.references.set(data['reference_ids'])
            
            return Response(
                CompositionDetailSerializer(composition, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Template View for Composition Builder UI
def composition_builder_view(request):
    """
    Serve the composition builder HTML template
    """
    return render(request, 'composition_builder.html')

# Data Management Views
class DataManagerView(APIView):
    """
    Comprehensive data management view for bulk operations and relationship management
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Get data management dashboard information
        """
        try:
            # Get entity counts
            counts = {
                'domains': Domain.objects.count(),
                'subdomains': SubDomain.objects.count(),
                'phases': Phase.objects.count(),
                'concepts': Concept.objects.count(),
                'themes': Theme.objects.count(),
                'techniques': Technique.objects.count(),
                'tools': Tool.objects.count(),
                'components': Component.objects.count(),
                'references': Reference.objects.count(),
                'compositions': Composition.objects.count(),
            }
            
            # Get relationship map
            relationship_map = self._get_relationship_map()
            
            return Response({
                'counts': counts,
                'relationship_map': relationship_map,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """
        Bulk create entities
        """
        try:
            entity_type = request.data.get('entity_type')
            entities_data = request.data.get('entities', [])
            
            if not entity_type or not entities_data:
                return Response({
                    'error': 'entity_type and entities are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            created_entities = []
            errors = []
            
            for i, entity_data in enumerate(entities_data):
                try:
                    entity = self._create_entity(entity_type, entity_data)
                    created_entities.append(entity)
                except Exception as e:
                    errors.append({
                        'index': i,
                        'data': entity_data,
                        'error': str(e)
                    })
            
            return Response({
                'created_count': len(created_entities),
                'error_count': len(errors),
                'created_entities': created_entities,
                'errors': errors,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        """
        Update a single entity
        """
        try:
            entity_type = request.data.get('entity_type')
            entity_id = request.data.get('entity_id')
            update_data = request.data.get('update_data', {})
            
            if not entity_type or not entity_id or not update_data:
                return Response({
                    'error': 'entity_type, entity_id, and update_data are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Prevent domain name updates
            if entity_type == 'domain' and 'name' in update_data:
                return Response({
                    'error': 'Domain name cannot be updated'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            updated_entity = self._update_entity(entity_type, entity_id, update_data)
            
            return Response({
                'updated_entity': updated_entity,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_relationship_map(self):
        """Get visual relationship map data"""
        domains = Domain.objects.prefetch_related(
            'sub_domains__phases__concepts__themes'
        ).all()
        
        relationship_map = []
        for domain in domains:
            domain_data = {
                'id': domain.id,
                'name': domain.name,
                'subdomains': []
            }
            
            for subdomain in domain.sub_domains.all():
                subdomain_data = {
                    'id': subdomain.id,
                    'name': subdomain.name,
                    'phases': []
                }
                
                for phase in subdomain.phases.all():
                    phase_data = {
                        'id': phase.id,
                        'name': phase.name,
                        'concepts': []
                    }
                    
                    for concept in phase.concepts.all():
                        concept_data = {
                            'id': concept.id,
                            'name': concept.name,
                            'themes': []
                        }
                        
                        for theme in concept.themes.all():
                            concept_data['themes'].append({
                                'id': theme.id,
                                'name': theme.name
                            })
                        
                        phase_data['concepts'].append(concept_data)
                    
                    subdomain_data['phases'].append(phase_data)
                
                domain_data['subdomains'].append(subdomain_data)
            
            relationship_map.append(domain_data)
        
        return relationship_map
    
    def _create_entity(self, entity_type, data):
        """Create a single entity based on type"""
        model_map = {
            'domain': Domain,
            'subdomain': SubDomain,
            'phase': Phase,
            'concept': Concept,
            'theme': Theme,
            'technique': Technique,
            'tool': Tool,
            'component': Component,
            'reference': Reference,
            'composition': Composition,
        }
        
        if entity_type not in model_map:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        model_class = model_map[entity_type]
        
        # Handle foreign key relationships
        if entity_type == 'subdomain' and 'domain_id' in data:
            data['domain'] = Domain.objects.get(id=data.pop('domain_id'))
        elif entity_type == 'phase' and 'subdomain_id' in data:
            data['subdomain'] = SubDomain.objects.get(id=data.pop('subdomain_id'))
        elif entity_type == 'concept' and 'phase_id' in data:
            data['phase'] = Phase.objects.get(id=data.pop('phase_id'))
        elif entity_type == 'theme' and 'concept_id' in data:
            data['concept'] = Concept.objects.get(id=data.pop('concept_id'))
        elif entity_type == 'technique' and 'phase_id' in data:
            data['phase'] = Phase.objects.get(id=data.pop('phase_id'))
        
        entity = model_class.objects.create(**data)
        return {
            'id': entity.id,
            'name': entity.name,
            'type': entity_type
        }
    
    def _update_entity(self, entity_type, entity_id, update_data):
        """Update a single entity based on type"""
        model_map = {
            'domain': Domain,
            'subdomain': SubDomain,
            'phase': Phase,
            'concept': Concept,
            'theme': Theme,
            'technique': Technique,
            'tool': Tool,
            'component': Component,
            'reference': Reference,
            'composition': Composition,
        }
        
        if entity_type not in model_map:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        model_class = model_map[entity_type]
        
        try:
            entity = model_class.objects.get(id=entity_id)
        except model_class.DoesNotExist:
            raise ValueError(f"{entity_type.title()} with id {entity_id} does not exist")
        
        # Handle foreign key relationships for updates
        if entity_type == 'subdomain' and 'domain_id' in update_data:
            update_data['domain'] = Domain.objects.get(id=update_data.pop('domain_id'))
        elif entity_type == 'phase' and 'subdomain_id' in update_data:
            update_data['subdomain'] = SubDomain.objects.get(id=update_data.pop('subdomain_id'))
        elif entity_type == 'concept' and 'phase_id' in update_data:
            update_data['phase'] = Phase.objects.get(id=update_data.pop('phase_id'))
        elif entity_type == 'theme' and 'concept_id' in update_data:
            update_data['concept'] = Concept.objects.get(id=update_data.pop('concept_id'))
        elif entity_type == 'technique' and 'phase_id' in update_data:
            update_data['phase'] = Phase.objects.get(id=update_data.pop('phase_id'))
        
        # Update the entity
        for key, value in update_data.items():
            setattr(entity, key, value)
        
        entity.save()
        
        return {
            'id': entity.id,
            'name': entity.name,
            'type': entity_type,
            'updated_fields': list(update_data.keys())
        }

class BulkImportView(APIView):
    """
    Handle bulk imports from various sources
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Import data from CSV, YouTube, or JSON
        """
        import_type = request.data.get('import_type')
        
        if import_type == 'csv':
            return self._import_csv(request)
        elif import_type == 'youtube':
            return self._import_youtube(request)
        elif import_type == 'json':
            return self._import_json(request)
        else:
            return Response({
                'error': 'Invalid import_type. Must be csv, youtube, or json'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _import_csv(self, request):
        """Import data from CSV file"""
        try:
            csv_file = request.FILES.get('csv_file')
            entity_type = request.data.get('entity_type')
            
            if not csv_file or not entity_type:
                return Response({
                    'error': 'csv_file and entity_type are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            import csv
            import io
            
            # Read CSV file
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            
            entities_data = list(csv_reader)
            
            # Create entities
            created_entities = []
            errors = []
            
            for i, row in enumerate(entities_data):
                try:
                    # Convert CSV row to entity data
                    entity_data = self._csv_row_to_entity_data(entity_type, row)
                    entity = self._create_entity_from_data(entity_type, entity_data)
                    created_entities.append(entity)
                except Exception as e:
                    errors.append({
                        'row': i + 1,
                        'data': row,
                        'error': str(e)
                    })
            
            return Response({
                'import_type': 'csv',
                'entity_type': entity_type,
                'created_count': len(created_entities),
                'error_count': len(errors),
                'created_entities': created_entities,
                'errors': errors,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _import_youtube(self, request):
        """Import references from YouTube playlist or video"""
        try:
            youtube_url = request.data.get('youtube_url')
            subdomain_id = request.data.get('subdomain_id')
            
            if not youtube_url:
                return Response({
                    'error': 'youtube_url is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract video ID(s) from URL
            video_ids = self._extract_youtube_ids(youtube_url)
            
            created_references = []
            errors = []
            
            for video_id in video_ids:
                try:
                    # Get video transcript
                    transcript = get_youtube_transcript(f"https://www.youtube.com/watch?v={video_id}")
                    
                    if transcript.startswith("Invalid") or transcript.startswith("Error"):
                        errors.append({
                            'video_id': video_id,
                            'error': transcript
                        })
                        continue
                    
                    # Create reference
                    reference_data = {
                        'name': f"YouTube Video {video_id}",
                        'description': f"Transcript from YouTube video: {video_id}",
                        'reference_type': 'youtube',
                        'content_url': f"https://www.youtube.com/watch?v={video_id}",
                        'raw_content': transcript
                    }
                    
                    if subdomain_id:
                        reference_data['subdomain'] = SubDomain.objects.get(id=subdomain_id)
                    
                    reference = Reference.objects.create(**reference_data)
                    created_references.append({
                        'id': reference.id,
                        'name': reference.name,
                        'video_id': video_id
                    })
                    
                except Exception as e:
                    errors.append({
                        'video_id': video_id,
                        'error': str(e)
                    })
            
            return Response({
                'import_type': 'youtube',
                'created_count': len(created_references),
                'error_count': len(errors),
                'created_references': created_references,
                'errors': errors,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _import_json(self, request):
        """Import data from JSON"""
        try:
            json_data = request.data.get('json_data')
            entity_type = request.data.get('entity_type')
            
            if not json_data or not entity_type:
                return Response({
                    'error': 'json_data and entity_type are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            import json
            
            if isinstance(json_data, str):
                entities_data = json.loads(json_data)
            else:
                entities_data = json_data
            
            created_entities = []
            errors = []
            
            for i, entity_data in enumerate(entities_data):
                try:
                    entity = self._create_entity_from_data(entity_type, entity_data)
                    created_entities.append(entity)
                except Exception as e:
                    errors.append({
                        'index': i,
                        'data': entity_data,
                        'error': str(e)
                    })
            
            return Response({
                'import_type': 'json',
                'entity_type': entity_type,
                'created_count': len(created_entities),
                'error_count': len(errors),
                'created_entities': created_entities,
                'errors': errors,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _csv_row_to_entity_data(self, entity_type, row):
        """Convert CSV row to entity data"""
        # Basic mapping - can be extended based on CSV structure
        entity_data = {}
        
        for key, value in row.items():
            if value.strip():  # Skip empty values
                entity_data[key.lower().replace(' ', '_')] = value.strip()
        
        return entity_data
    
    def _create_entity_from_data(self, entity_type, data):
        """Create entity from data (helper method)"""
        # This would use the same logic as DataManagerView._create_entity
        # For now, return a simple structure
        return {
            'type': entity_type,
            'data': data,
            'status': 'created'
        }
    
    def _extract_youtube_ids(self, url):
        """Extract YouTube video IDs from URL"""
        import re
        
        # Handle playlist URLs
        if 'playlist' in url:
            # For playlists, we'd need to use YouTube API
            # For now, return single video ID
            match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", url)
            return [match.group(1)] if match else []
        
        # Handle single video URLs
        match = re.search(r"(?:v=|\/embed\/|\/v\/|youtu\.be\/)([A-Za-z0-9_-]{11})", url)
        return [match.group(1)] if match else []

class DataExportView(APIView):
    """
    Handle data export operations
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        Export data in various formats
        """
        export_type = request.GET.get('type', 'json')
        entity_type = request.GET.get('entity_type')
        
        if export_type == 'csv':
            return self._export_csv(entity_type)
        elif export_type == 'json':
            return self._export_json(entity_type)
        else:
            return Response({
                'error': 'Invalid export type. Must be csv or json'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def _export_csv(self, entity_type):
        """Export data as CSV"""
        try:
            import csv
            import io
            
            # Get data based on entity type
            data = self._get_export_data(entity_type)
            
            if not data:
                return Response({
                    'error': 'No data found for export'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Create CSV
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            csv_content = output.getvalue()
            output.close()
            
            return Response({
                'export_type': 'csv',
                'entity_type': entity_type,
                'data': csv_content,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _export_json(self, entity_type):
        """Export data as JSON"""
        try:
            data = self._get_export_data(entity_type)
            
            return Response({
                'export_type': 'json',
                'entity_type': entity_type,
                'data': data,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_export_data(self, entity_type):
        """Get data for export"""
        model_map = {
            'domain': Domain,
            'subdomain': SubDomain,
            'phase': Phase,
            'concept': Concept,
            'theme': Theme,
            'technique': Technique,
            'tool': Tool,
            'component': Component,
            'reference': Reference,
            'composition': Composition,
        }
        
        if entity_type and entity_type in model_map:
            model_class = model_map[entity_type]
            return list(model_class.objects.values())
        else:
            # Export all data
            all_data = {}
            for name, model_class in model_map.items():
                all_data[name] = list(model_class.objects.values())
            return all_data

class EntityListView(APIView):
    """
    List entities by type for selection
    """
    permission_classes = [AllowAny]
    
    def get(self, request, entity_type):
        """
        Get list of entities of a specific type
        """
        try:
            model_map = {
                'domain': Domain,
                'subdomain': SubDomain,
                'phase': Phase,
                'concept': Concept,
                'theme': Theme,
                'technique': Technique,
                'tool': Tool,
                'component': Component,
                'reference': Reference,
                'composition': Composition,
            }
            
            if entity_type not in model_map:
                return Response({
                    'error': f'Unknown entity type: {entity_type}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            model_class = model_map[entity_type]
            entities = model_class.objects.all().order_by('name')
            
            entity_list = []
            for entity in entities:
                entity_data = {
                    'id': entity.id,
                    'name': entity.name,
                    'description': entity.description[:100] + '...' if len(entity.description) > 100 else entity.description,
                }
                
                # Add entity-specific info for context
                if entity_type == 'subdomain' and entity.domain:
                    entity_data['parent'] = f"Domain: {entity.domain.name}"
                elif entity_type == 'phase' and entity.sub_domain:
                    entity_data['parent'] = f"SubDomain: {entity.sub_domain.name}"
                elif entity_type == 'concept' and entity.phase:
                    entity_data['parent'] = f"Phase: {entity.phase.name}"
                elif entity_type == 'theme' and entity.concept:
                    entity_data['parent'] = f"Concept: {entity.concept.name}"
                elif entity_type == 'technique' and entity.phase:
                    entity_data['parent'] = f"Phase: {entity.phase.name}"
                elif entity_type == 'tool':
                    entity_data['parent'] = f"Platform: {entity.get_software_platform_display()}"
                elif entity_type == 'component':
                    entity_data['parent'] = f"Type: {entity.get_component_type_display()}"
                elif entity_type == 'reference':
                    entity_data['parent'] = f"Type: {entity.get_reference_type_display()}"
                
                entity_list.append(entity_data)
            
            return Response({
                'entities': entity_list,
                'entity_type': entity_type,
                'count': len(entity_list),
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EntityDetailView(APIView):
    """
    Get individual entity details for editing
    """
    permission_classes = [AllowAny]
    
    def get(self, request, entity_type, entity_id):
        """
        Get details of a specific entity
        """
        try:
            model_map = {
                'domain': Domain,
                'subdomain': SubDomain,
                'phase': Phase,
                'concept': Concept,
                'theme': Theme,
                'technique': Technique,
                'tool': Tool,
                'component': Component,
                'reference': Reference,
                'composition': Composition,
            }
            
            if entity_type not in model_map:
                return Response({
                    'error': f'Unknown entity type: {entity_type}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            model_class = model_map[entity_type]
            
            try:
                entity = model_class.objects.get(id=entity_id)
            except model_class.DoesNotExist:
                return Response({
                    'error': f'{entity_type.title()} with id {entity_id} does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Convert entity to dictionary
            entity_data = {
                'id': entity.id,
                'name': entity.name,
                'description': entity.description,
                'created_at': entity.created_at,
                'updated_at': entity.updated_at,
            }
            
            # Add entity-specific fields
            if entity_type == 'domain':
                entity_data.update({
                    'icon': entity.icon,
                    'is_active': entity.is_active,
                })
            elif entity_type == 'subdomain':
                entity_data.update({
                    'domain_id': entity.domain.id if entity.domain else None,
                    'domain_name': entity.domain.name if entity.domain else None,
                })
            elif entity_type == 'phase':
                entity_data.update({
                    'subdomain_id': entity.sub_domain.id if entity.sub_domain else None,
                    'subdomain_name': entity.sub_domain.name if entity.sub_domain else None,
                })
            elif entity_type == 'concept':
                entity_data.update({
                    'domain_id': entity.domain.id if entity.domain else None,
                    'domain_name': entity.domain.name if entity.domain else None,
                    'subdomain_id': entity.sub_domain.id if entity.sub_domain else None,
                    'subdomain_name': entity.sub_domain.name if entity.sub_domain else None,
                    'phase_id': entity.phase.id if entity.phase else None,
                    'phase_name': entity.phase.name if entity.phase else None,
                })
            elif entity_type == 'theme':
                entity_data.update({
                    'concept_id': entity.concept.id if entity.concept else None,
                    'concept_name': entity.concept.name if entity.concept else None,
                })
            elif entity_type == 'technique':
                entity_data.update({
                    'phase_id': entity.phase.id if entity.phase else None,
                    'phase_name': entity.phase.name if entity.phase else None,
                    'category': entity.category,
                    'outcome': entity.outcome,
                    'estimated_time': str(entity.estimated_time) if entity.estimated_time else None,
                    'usage_frequency': entity.usage_frequency,
                })
            elif entity_type == 'tool':
                entity_data.update({
                    'tool_type': entity.tool_type,
                    'software_platform': entity.software_platform,
                    'category': entity.category,
                    'keyboard_shortcut': entity.keyboard_shortcut,
                })
            elif entity_type == 'component':
                entity_data.update({
                    'component_type': entity.component_type,
                    'file_format': entity.file_format,
                })
            elif entity_type == 'reference':
                entity_data.update({
                    'reference_type': entity.reference_type,
                    'content_url': entity.content_url,
                    'file_path': entity.file_path,
                    'timestamp_start': str(entity.timestamp_start) if entity.timestamp_start else None,
                    'timestamp_end': str(entity.timestamp_end) if entity.timestamp_end else None,
                    'thumbnail_url': entity.thumbnail_url,
                    'quality_rating': entity.quality_rating,
                    'subdomain_id': entity.sub_domain.id if entity.sub_domain else None,
                    'subdomain_name': entity.sub_domain.name if entity.sub_domain else None,
                })
            
            return Response({
                'entity': entity_data,
                'entity_type': entity_type,
                'status': 'success'
            })
            
        except Exception as e:
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Template View for Data Manager UI
def data_manager_view(request):
    """
    Serve the data manager HTML template
    """
    return render(request, 'data_manager.html')