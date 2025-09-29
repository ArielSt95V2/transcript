# serializers.py
# In Django REST Framework, you need serializers to convert between Python objects and JSON for your API

from rest_framework import serializers
from .models import Domain, SubDomain, Phase, Concept, Theme, Reference, Component, Tool, Technique, Composition

# Base serializer with common fields
class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer that all other serializers can inherit from"""
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        abstract = True


# Domain Serializers
class DomainListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    sub_domains_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Domain
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'sub_domains_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_sub_domains_count(self, obj):
        return obj.sub_domains.count()

class DomainDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views with related data"""
    sub_domains = serializers.SerializerMethodField()
    
    class Meta:
        model = Domain
        fields = ['id', 'name', 'description', 'icon', 'is_active', 'sub_domains', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_sub_domains(self, obj):
        sub_domains = obj.sub_domains.all()[:10]  # Limit to avoid large payloads
        return SubDomainListSerializer(sub_domains, many=True, context=self.context).data

class DomainCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating domains"""
    class Meta:
        model = Domain
        fields = ['name', 'description', 'icon', 'is_active']
    
    def validate_name(self, value):
        """Validate domain name length"""
        value = value.strip()
        
        if len(value) < 2:
            raise serializers.ValidationError("Domain name must be at least 2 characters long")
        
        return value

# SubDomain Serializers
class SubDomainListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    phases_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SubDomain
        fields = ['id', 'name', 'description', 'domain_name', 'phases_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_phases_count(self, obj):
        return obj.phases.count()

class SubDomainDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    domain = DomainListSerializer(read_only=True)
    phases = serializers.SerializerMethodField()
    
    class Meta:
        model = SubDomain
        fields = ['id', 'name', 'description', 'domain', 'phases', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_phases(self, obj):
        phases = obj.phases.all()[:10]
        return PhaseListSerializer(phases, many=True, context=self.context).data

class SubDomainCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating subdomains"""
    class Meta:
        model = SubDomain
        fields = ['name', 'description', 'domain']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("SubDomain name must be at least 2 characters long")
        return value.strip()
    
# Phase Serializers
class PhaseListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    sub_domain_name = serializers.CharField(source='sub_domain.name', read_only=True)
    techniques_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Phase
        fields = ['id', 'name', 'description', 'sub_domain_name', 'techniques_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques_count(self, obj):
        return obj.techniques.count()

class PhaseDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    sub_domain = SubDomainListSerializer(read_only=True)
    techniques = serializers.SerializerMethodField()
    
    class Meta:
        model = Phase
        fields = ['id', 'name', 'description', 'sub_domain', 'techniques', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_techniques(self, obj):
        techniques = obj.techniques.all()[:10]
        return TechniqueListSerializer(techniques, many=True, context=self.context).data

class PhaseCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating phases"""
    class Meta:
        model = Phase
        fields = ['name', 'description', 'sub_domain']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Phase name must be at least 2 characters long")
        return value.strip()

# Concept Serializers
class ConceptListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    sub_domain_name = serializers.CharField(source='sub_domain.name', read_only=True)
    phase_name = serializers.CharField(source='phase.name', read_only=True)
    themes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Concept
        fields = ['id', 'name', 'description', 'domain_name', 'sub_domain_name', 'phase_name', 'themes_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_themes_count(self, obj):
        return obj.themes.count()

class ConceptDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    domain = DomainListSerializer(read_only=True)
    sub_domain = SubDomainListSerializer(read_only=True)
    phase = PhaseListSerializer(read_only=True)
    themes = serializers.SerializerMethodField()
    
    class Meta:
        model = Concept
        fields = ['id', 'name', 'description', 'domain', 'sub_domain', 'phase', 'themes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_themes(self, obj):
        themes = obj.themes.all()[:10]
        return ThemeListSerializer(themes, many=True, context=self.context).data

class ConceptCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating concepts"""
    class Meta:
        model = Concept
        fields = ['name', 'description', 'domain', 'sub_domain', 'phase']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Concept name must be at least 2 characters long")
        return value.strip()
    
    def validate(self, data):
        # Ensure domain, sub_domain, and phase are consistent
        domain = data.get('domain')
        sub_domain = data.get('sub_domain')
        phase = data.get('phase')
        
        if domain and sub_domain and sub_domain.domain != domain:
            raise serializers.ValidationError("SubDomain must belong to the selected Domain")
        
        if sub_domain and phase and phase.sub_domain != sub_domain:
            raise serializers.ValidationError("Phase must belong to the selected SubDomain")
        
        return data

# Theme Serializers
class ThemeListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    sub_domain_name = serializers.CharField(source='sub_domain.name', read_only=True)
    phase_name = serializers.CharField(source='phase.name', read_only=True)
    techniques_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Theme
        fields = ['id', 'name', 'description', 'domain_name', 'sub_domain_name', 'phase_name', 'techniques_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques_count(self, obj):
        return obj.techniques.count()

class ThemeDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    domain = DomainListSerializer(read_only=True)
    sub_domain = SubDomainListSerializer(read_only=True)
    phase = PhaseListSerializer(read_only=True)
    techniques = serializers.SerializerMethodField()
    
    class Meta:
        model = Theme
        fields = ['id', 'name', 'description', 'domain', 'sub_domain', 'phase', 'techniques', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques(self, obj):
        techniques = obj.techniques.all()[:10]
        return TechniqueListSerializer(techniques, many=True, context=self.context).data

class ThemeCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating themes"""
    class Meta:
        model = Theme
        fields = ['name', 'description', 'domain', 'sub_domain', 'phase']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Theme name must be at least 2 characters long")
        return value.strip()

# Reference Serializers
class ReferenceListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    reference_type_display = serializers.CharField(source='get_reference_type_display', read_only=True)
    sub_domain_name = serializers.CharField(source='sub_domain.name', read_only=True)
    
    class Meta:
        model = Reference
        fields = ['id', 'name', 'description', 'reference_type', 'reference_type_display', 'sub_domain_name', 'quality_rating', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReferenceDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    reference_type_display = serializers.CharField(source='get_reference_type_display', read_only=True)
    sub_domain = SubDomainListSerializer(read_only=True)
    
    class Meta:
        model = Reference
        fields = ['id', 'name', 'description', 'reference_type', 'reference_type_display', 'content_url', 'file_path', 'timestamp_start', 'timestamp_end', 'thumbnail_url', 'quality_rating', 'sub_domain', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReferenceCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating references"""
    class Meta:
        model = Reference
        fields = ['name', 'description', 'reference_type', 'content_url', 'file_path', 'timestamp_start', 'timestamp_end', 'thumbnail_url', 'quality_rating', 'sub_domain']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Reference name must be at least 2 characters long")
        return value.strip()
    
    def validate(self, data):
        # Ensure either content_url or file_path is provided
        if not data.get('content_url') and not data.get('file_path'):
            raise serializers.ValidationError("Either content_url or file_path must be provided")
        return data

# Component Serializers
class ComponentListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    component_type_display = serializers.CharField(source='get_component_type_display', read_only=True)
    techniques_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'description', 'component_type', 'component_type_display', 'file_format', 'techniques_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques_count(self, obj):
        return obj.techniques.count()

class ComponentDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    component_type_display = serializers.CharField(source='get_component_type_display', read_only=True)
    techniques = serializers.SerializerMethodField()
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'description', 'component_type', 'component_type_display', 'file_format', 'techniques', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques(self, obj):
        techniques = obj.techniques.all()[:10]
        return TechniqueListSerializer(techniques, many=True, context=self.context).data

class ComponentCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating components"""
    class Meta:
        model = Component
        fields = ['name', 'description', 'component_type', 'file_format']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Component name must be at least 2 characters long")
        return value.strip()

# Tool Serializers
class ToolListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    tool_type_display = serializers.CharField(source='get_tool_type_display', read_only=True)
    software_platform_display = serializers.CharField(source='get_software_platform_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    techniques_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'tool_type', 'tool_type_display', 'software_platform', 'software_platform_display', 'category', 'category_display', 'keyboard_shortcut', 'techniques_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques_count(self, obj):
        return obj.techniques.count()

class ToolDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    tool_type_display = serializers.CharField(source='get_tool_type_display', read_only=True)
    software_platform_display = serializers.CharField(source='get_software_platform_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    techniques = serializers.SerializerMethodField()
    
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'tool_type', 'tool_type_display', 'software_platform', 'software_platform_display', 'category', 'category_display', 'keyboard_shortcut', 'techniques', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_techniques(self, obj):
        techniques = obj.techniques.all()[:10]
        return TechniqueListSerializer(techniques, many=True, context=self.context).data

class ToolCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating tools"""
    class Meta:
        model = Tool
        fields = ['name', 'description', 'tool_type', 'software_platform', 'category', 'keyboard_shortcut']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Tool name must be at least 2 characters long")
        return value.strip()

# Technique Serializers
class TechniqueListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    phase_name = serializers.CharField(source='phase.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    themes_count = serializers.SerializerMethodField()
    tools_count = serializers.SerializerMethodField()
    components_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Technique
        fields = ['id', 'name', 'description', 'phase_name', 'category', 'category_display', 'outcome', 'estimated_time', 'usage_frequency', 'themes_count', 'tools_count', 'components_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_themes_count(self, obj):
        return obj.themes.count()
    
    def get_tools_count(self, obj):
        return obj.tools.count()
    
    def get_components_count(self, obj):
        return obj.components.count()

class TechniqueDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views with nested relationships"""
    phase = PhaseListSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    themes = ThemeListSerializer(many=True, read_only=True)
    tools = ToolListSerializer(many=True, read_only=True)
    components = ComponentListSerializer(many=True, read_only=True)
    references = ReferenceListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Technique
        fields = ['id', 'name', 'description', 'phase', 'category', 'category_display', 'outcome', 'instructions', 'tools_used', 'estimated_time', 'usage_frequency', 'themes', 'tools', 'components', 'references', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TechniqueCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating techniques"""
    class Meta:
        model = Technique
        fields = ['name', 'description', 'phase', 'category', 'outcome', 'instructions', 'tools_used', 'estimated_time', 'usage_frequency', 'themes', 'tools', 'components', 'references']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Technique name must be at least 2 characters long")
        return value.strip()
    
    def validate_outcome(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Outcome must be at least 10 characters long")
        return value.strip()

# Composition Serializers
class CompositionListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    sub_domain_name = serializers.CharField(source='sub_domain.name', read_only=True)
    phase_name = serializers.CharField(source='phase.name', read_only=True)
    technique_name = serializers.CharField(source='technique.name', read_only=True)
    tool_name = serializers.CharField(source='tool.name', read_only=True)
    component_name = serializers.CharField(source='component.name', read_only=True)
    reference_name = serializers.CharField(source='reference.name', read_only=True)
    
    class Meta:
        model = Composition
        fields = ['id', 'name', 'description', 'domain_name', 'sub_domain_name', 'phase_name', 'technique_name', 'tool_name', 'component_name', 'reference_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CompositionDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    domain = DomainListSerializer(read_only=True)
    sub_domain = SubDomainListSerializer(read_only=True)
    phase = PhaseListSerializer(read_only=True)
    technique = TechniqueListSerializer(read_only=True)
    tool = ToolListSerializer(read_only=True)
    component = ComponentListSerializer(read_only=True)
    reference = ReferenceListSerializer(read_only=True)
    
    class Meta:
        model = Composition
        fields = ['id', 'name', 'description', 'domain', 'sub_domain', 'phase', 'technique', 'tool', 'component', 'reference', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CompositionCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating compositions"""
    class Meta:
        model = Composition
        fields = ['name', 'description', 'domain', 'sub_domain', 'phase', 'technique', 'tool', 'component', 'reference']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Composition name must be at least 2 characters long")
        return value.strip()

