from django.contrib import admin
from .models import Domain, SubDomain, Phase, Concept, Theme, Reference, Component, Tool, Technique, Composition

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon', 'is_active', 'sub_domains_count', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def sub_domains_count(self, obj):
        """Show how many subdomains are linked to this domain"""
        return obj.sub_domains.count()
    sub_domains_count.short_description = "Sub Domains"

@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'domain', 'phases_count', 'created_at', 'updated_at']
    list_filter = ['domain', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'domain__name']
    ordering = ['domain', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def phases_count(self, obj):
        """Show how many phases are linked to this subdomain"""
        return obj.phases.count()
    phases_count.short_description = "Phases"

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'sub_domain', 'concepts_count', 'techniques_count', 'created_at', 'updated_at']
    list_filter = ['sub_domain__domain', 'sub_domain', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'sub_domain__name']
    ordering = ['sub_domain', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def concepts_count(self, obj):
        """Show how many concepts are linked to this phase"""
        return obj.concepts.count()
    concepts_count.short_description = "Concepts"
    
    def techniques_count(self, obj):
        """Show how many techniques are linked to this phase"""
        return obj.techniques.count()
    techniques_count.short_description = "Techniques"

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'domain', 'sub_domain', 'phase', 'themes_count', 'created_at', 'updated_at']
    list_filter = ['domain', 'sub_domain', 'phase', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['domain', 'sub_domain', 'phase', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def themes_count(self, obj):
        """Show how many themes are linked to this concept"""
        return obj.themes.count()
    themes_count.short_description = "Themes"

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'concept', 'techniques_count', 'created_at', 'updated_at']
    list_filter = ['concept__domain', 'concept__sub_domain', 'concept__phase', 'concept', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'concept__name']
    ordering = ['concept', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def techniques_count(self, obj):
        """Show how many techniques are linked to this theme"""
        return obj.techniques.count()
    techniques_count.short_description = "Techniques"

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'reference_type', 'sub_domain', 'quality_rating', 'content_preview', 'created_at', 'updated_at']
    list_filter = ['reference_type', 'quality_rating', 'sub_domain', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'content_url', 'file_path']
    ordering = ['-quality_rating', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        """Show content URL or file path preview"""
        if obj.content_url:
            return f"URL: {obj.content_url[:50]}..." if len(obj.content_url) > 50 else f"URL: {obj.content_url}"
        elif obj.file_path:
            return f"File: {obj.file_path[:50]}..." if len(obj.file_path) > 50 else f"File: {obj.file_path}"
        return "No content"
    content_preview.short_description = "Content Preview"

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'component_type', 'file_format', 'techniques_count', 'created_at', 'updated_at']
    list_filter = ['component_type', 'file_format', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'component_type']
    ordering = ['component_type', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def techniques_count(self, obj):
        """Show how many techniques use this component"""
        return obj.techniques.count()
    techniques_count.short_description = "Techniques"

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'tool_type', 'software_platform', 'category', 'keyboard_shortcut', 'techniques_count', 'created_at', 'updated_at']
    list_filter = ['tool_type', 'software_platform', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'keyboard_shortcut']
    ordering = ['software_platform', 'category', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def techniques_count(self, obj):
        """Show how many techniques use this tool"""
        return obj.techniques.count()
    techniques_count.short_description = "Techniques"

@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'phase', 'category', 'outcome_preview', 'estimated_time', 'usage_frequency', 'themes_count', 'tools_count', 'components_count', 'created_at', 'updated_at']
    list_filter = ['category', 'phase__sub_domain__domain', 'phase__sub_domain', 'phase', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'outcome']
    ordering = ['phase', 'category', 'name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['themes', 'tools', 'components', 'references']  # Better UI for many-to-many relationships
    
    def outcome_preview(self, obj):
        """Show first 100 characters of outcome"""
        if obj.outcome:
            return obj.outcome[:100] + "..." if len(obj.outcome) > 100 else obj.outcome
        return "No outcome"
    outcome_preview.short_description = "Outcome Preview"
    
    def themes_count(self, obj):
        """Show how many themes are linked to this technique"""
        return obj.themes.count()
    themes_count.short_description = "Themes"
    
    def tools_count(self, obj):
        """Show how many tools are linked to this technique"""
        return obj.tools.count()
    tools_count.short_description = "Tools"
    
    def components_count(self, obj):
        """Show how many components are linked to this technique"""
        return obj.components.count()
    components_count.short_description = "Components"

@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'domain', 'sub_domain', 'phase', 'concept', 'theme', 'techniques_count', 'tools_count', 'components_count', 'references_count', 'created_at', 'updated_at']
    list_filter = ['domain', 'sub_domain', 'phase', 'concept', 'theme', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['technique', 'tools', 'components', 'references']  # Better UI for many-to-many relationships
    
    def techniques_count(self, obj):
        """Show how many techniques are in this composition"""
        return obj.technique.count()
    techniques_count.short_description = "Techniques"
    
    def tools_count(self, obj):
        """Show how many tools are in this composition"""
        return obj.tools.count()
    tools_count.short_description = "Tools"
    
    def components_count(self, obj):
        """Show how many components are in this composition"""
        return obj.components.count()
    components_count.short_description = "Components"
    
    def references_count(self, obj):
        """Show how many references are in this composition"""
        return obj.references.count()
    references_count.short_description = "References"

# Customize admin site header and title
admin.site.site_header = "Video Editing Knowledge Base Admin"
admin.site.site_title = "VEKB Admin"
admin.site.index_title = "Welcome to Video Editing Knowledge Base Administration"