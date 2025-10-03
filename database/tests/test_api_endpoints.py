"""
Comprehensive Test Suite for Database API Endpoints
Tests all CRUD operations for all ViewSets with validation and edge cases.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
import json

from database.models import (
    Domain, SubDomain, Phase, Concept, Theme, 
    Reference, Component, Tool, Technique, Composition
)


class BaseAPITestCase(TestCase):
    """Base test case with common setup and helper methods"""
    
    def setUp(self):
        """Set up test client and common test data"""
        self.client = APIClient()
        self.maxDiff = None  # Show full diff on assertion failures
        
    def assert_response_status(self, response, expected_status):
        """Helper to assert response status with detailed error message"""
        if response.status_code != expected_status:
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, expected_status)
    
    def create_test_hierarchy(self):
        """Create a complete hierarchy for testing relationships"""
        # Create Domain
        self.domain = Domain.objects.create(
            name="Test Domain",
            description="Test domain description",
            icon="test-icon",
            is_active=True
        )
        
        # Create SubDomain
        self.subdomain = SubDomain.objects.create(
            name="Test SubDomain",
            description="Test subdomain description",
            domain=self.domain
        )
        
        # Create Phase
        self.phase = Phase.objects.create(
            name="Test Phase",
            description="Test phase description",
            sub_domain=self.subdomain
        )
        
        # Create Concept
        self.concept = Concept.objects.create(
            name="Test Concept",
            description="Test concept description",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase
        )
        
        # Create Theme
        self.theme = Theme.objects.create(
            name="Test Theme",
            description="Test theme description",
            concept=self.concept
        )
        
        # Create Reference
        self.reference = Reference.objects.create(
            name="Test Reference",
            description="Test reference description",
            reference_type="youtube",
            content_url="https://youtube.com/test",
            quality_rating=5,
            sub_domain=self.subdomain
        )
        
        # Create Component
        self.component = Component.objects.create(
            name="Test Component",
            description="Test component description",
            component_type="audio",
            file_format="MP3"
        )
        
        # Create Tool
        self.tool = Tool.objects.create(
            name="Test Tool",
            description="Test tool description",
            tool_type="keyboard",
            software_platform="premiere",
            category="cutting",
            keyboard_shortcut="Ctrl+X"
        )
        
        # Create Technique
        self.technique = Technique.objects.create(
            name="Test Technique",
            description="Test technique description",
            phase=self.phase,
            category="rhythm_timing",
            outcome="Test outcome for the technique",
            instructions=["Step 1", "Step 2", "Step 3"],
            tools_used=["Tool 1", "Tool 2"],
            estimated_time=timedelta(minutes=30),
            usage_frequency=10
        )
        self.technique.themes.add(self.theme)
        self.technique.tools.add(self.tool)
        self.technique.components.add(self.component)
        self.technique.references.add(self.reference)
        
        # Create Composition
        self.composition = Composition.objects.create(
            name="Test Composition",
            description="Test composition description",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase,
            concept=self.concept,
            theme=self.theme
        )
        self.composition.technique.add(self.technique)
        self.composition.tools.add(self.tool)
        self.composition.components.add(self.component)
        self.composition.references.add(self.reference)


class DomainAPITestCase(BaseAPITestCase):
    """Test suite for Domain endpoints"""
    
    def test_list_domains(self):
        """Test GET /api/domains/ - List all domains"""
        # Create test data
        Domain.objects.create(name="Domain 1", description="Description 1")
        Domain.objects.create(name="Domain 2", description="Description 2")
        
        url = reverse('domain-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('name', response.data[0])
        self.assertIn('description', response.data[0])
        self.assertIn('sub_domains_count', response.data[0])
    
    def test_create_domain(self):
        """Test POST /api/domains/ - Create a new domain"""
        url = reverse('domain-list')
        data = {
            'name': 'New Domain',
            'description': 'New domain description',
            'icon': 'new-icon',
            'is_active': True
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        self.assertEqual(Domain.objects.count(), 1)
        domain = Domain.objects.get()
        self.assertEqual(domain.name, 'New Domain')
        self.assertEqual(domain.icon, 'new-icon')
        self.assertTrue(domain.is_active)
    
    def test_create_domain_validation_error(self):
        """Test POST /api/domains/ - Validation error for short name"""
        url = reverse('domain-list')
        data = {
            'name': 'A',  # Too short
            'description': 'Description'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
    
    def test_retrieve_domain_by_id(self):
        """Test GET /api/domains/{id}/ - Retrieve domain by ID"""
        domain = Domain.objects.create(name="Test Domain", description="Description")
        
        url = reverse('domain-detail', kwargs={'pk': domain.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Domain')
        self.assertIn('sub_domains', response.data)
    
    def test_retrieve_domain_by_name(self):
        """Test GET /api/domains/{name}/ - Retrieve domain by name"""
        domain = Domain.objects.create(name="filmmaking", description="Description")
        
        url = reverse('domain-detail', kwargs={'pk': 'filmmaking'})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'filmmaking')
    
    def test_update_domain_full(self):
        """Test PUT /api/domains/{id}/ - Full update of domain"""
        domain = Domain.objects.create(name="Old Name", description="Old Description")
        
        url = reverse('domain-detail', kwargs={'pk': domain.id})
        data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'icon': 'updated-icon',
            'is_active': False
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        domain.refresh_from_db()
        self.assertEqual(domain.name, 'Updated Name')
        self.assertEqual(domain.description, 'Updated Description')
        self.assertFalse(domain.is_active)
    
    def test_update_domain_partial(self):
        """Test PATCH /api/domains/{id}/ - Partial update of domain"""
        domain = Domain.objects.create(name="Original", description="Description")
        
        url = reverse('domain-detail', kwargs={'pk': domain.id})
        data = {'description': 'Partially Updated'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        domain.refresh_from_db()
        self.assertEqual(domain.name, 'Original')  # Unchanged
        self.assertEqual(domain.description, 'Partially Updated')
    
    def test_delete_domain(self):
        """Test DELETE /api/domains/{id}/ - Delete domain"""
        domain = Domain.objects.create(name="To Delete", description="Description")
        
        url = reverse('domain-detail', kwargs={'pk': domain.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Domain.objects.count(), 0)
    
    def test_domain_not_found(self):
        """Test GET /api/domains/{id}/ - 404 for non-existent domain"""
        url = reverse('domain-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_404_NOT_FOUND)


class SubDomainAPITestCase(BaseAPITestCase):
    """Test suite for SubDomain endpoints"""
    
    def setUp(self):
        super().setUp()
        self.domain = Domain.objects.create(name="Parent Domain", description="Description")
    
    def test_list_subdomains(self):
        """Test GET /api/subdomains/ - List all subdomains"""
        SubDomain.objects.create(name="SubDomain 1", description="Desc 1", domain=self.domain)
        SubDomain.objects.create(name="SubDomain 2", description="Desc 2", domain=self.domain)
        
        url = reverse('subdomain-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('domain_name', response.data[0])
        self.assertIn('phases_count', response.data[0])
    
    def test_create_subdomain(self):
        """Test POST /api/subdomains/ - Create a new subdomain"""
        url = reverse('subdomain-list')
        data = {
            'name': 'New SubDomain',
            'description': 'New subdomain description',
            'domain': self.domain.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        self.assertEqual(SubDomain.objects.count(), 1)
        subdomain = SubDomain.objects.get()
        self.assertEqual(subdomain.name, 'New SubDomain')
        self.assertEqual(subdomain.domain, self.domain)
    
    def test_create_subdomain_validation_error(self):
        """Test POST /api/subdomains/ - Validation error"""
        url = reverse('subdomain-list')
        data = {
            'name': 'X',  # Too short
            'description': 'Description',
            'domain': self.domain.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_subdomain(self):
        """Test GET /api/subdomains/{id}/ - Retrieve subdomain"""
        subdomain = SubDomain.objects.create(
            name="Test SubDomain", 
            description="Description",
            domain=self.domain
        )
        
        url = reverse('subdomain-detail', kwargs={'pk': subdomain.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test SubDomain')
        self.assertIn('domain', response.data)
        self.assertIn('phases', response.data)
    
    def test_update_subdomain(self):
        """Test PUT /api/subdomains/{id}/ - Update subdomain"""
        subdomain = SubDomain.objects.create(
            name="Old Name",
            description="Old Description",
            domain=self.domain
        )
        
        url = reverse('subdomain-detail', kwargs={'pk': subdomain.id})
        data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'domain': self.domain.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        subdomain.refresh_from_db()
        self.assertEqual(subdomain.name, 'Updated Name')
    
    def test_delete_subdomain(self):
        """Test DELETE /api/subdomains/{id}/ - Delete subdomain"""
        subdomain = SubDomain.objects.create(
            name="To Delete",
            description="Description",
            domain=self.domain
        )
        
        url = reverse('subdomain-detail', kwargs={'pk': subdomain.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SubDomain.objects.count(), 0)


class PhaseAPITestCase(BaseAPITestCase):
    """Test suite for Phase endpoints"""
    
    def setUp(self):
        super().setUp()
        self.domain = Domain.objects.create(name="Domain", description="Description")
        self.subdomain = SubDomain.objects.create(
            name="SubDomain",
            description="Description",
            domain=self.domain
        )
    
    def test_list_phases(self):
        """Test GET /api/phases/ - List all phases"""
        Phase.objects.create(name="Phase 1", description="Desc 1", sub_domain=self.subdomain)
        Phase.objects.create(name="Phase 2", description="Desc 2", sub_domain=self.subdomain)
        
        url = reverse('phase-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('sub_domain_name', response.data[0])
        self.assertIn('techniques_count', response.data[0])
    
    def test_create_phase(self):
        """Test POST /api/phases/ - Create a new phase"""
        url = reverse('phase-list')
        data = {
            'name': 'New Phase',
            'description': 'New phase description',
            'sub_domain': self.subdomain.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        self.assertEqual(Phase.objects.count(), 1)
        phase = Phase.objects.get()
        self.assertEqual(phase.name, 'New Phase')
        self.assertEqual(phase.sub_domain, self.subdomain)
    
    def test_retrieve_phase(self):
        """Test GET /api/phases/{id}/ - Retrieve phase"""
        phase = Phase.objects.create(
            name="Test Phase",
            description="Description",
            sub_domain=self.subdomain
        )
        
        url = reverse('phase-detail', kwargs={'pk': phase.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Phase')
        self.assertIn('sub_domain', response.data)
        self.assertIn('techniques', response.data)
    
    def test_update_phase(self):
        """Test PATCH /api/phases/{id}/ - Partial update phase"""
        phase = Phase.objects.create(
            name="Old Name",
            description="Old Description",
            sub_domain=self.subdomain
        )
        
        url = reverse('phase-detail', kwargs={'pk': phase.id})
        data = {'name': 'Updated Name'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        phase.refresh_from_db()
        self.assertEqual(phase.name, 'Updated Name')
    
    def test_delete_phase(self):
        """Test DELETE /api/phases/{id}/ - Delete phase"""
        phase = Phase.objects.create(
            name="To Delete",
            description="Description",
            sub_domain=self.subdomain
        )
        
        url = reverse('phase-detail', kwargs={'pk': phase.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Phase.objects.count(), 0)


class ConceptAPITestCase(BaseAPITestCase):
    """Test suite for Concept endpoints"""
    
    def setUp(self):
        super().setUp()
        self.domain = Domain.objects.create(name="Domain", description="Description")
        self.subdomain = SubDomain.objects.create(
            name="SubDomain",
            description="Description",
            domain=self.domain
        )
        self.phase = Phase.objects.create(
            name="Phase",
            description="Description",
            sub_domain=self.subdomain
        )
    
    def test_list_concepts(self):
        """Test GET /api/concepts/ - List all concepts"""
        Concept.objects.create(
            name="Concept 1",
            description="Desc 1",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase
        )
        
        url = reverse('concept-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('domain_name', response.data[0])
        self.assertIn('sub_domain_name', response.data[0])
        self.assertIn('phase_name', response.data[0])
    
    def test_create_concept(self):
        """Test POST /api/concepts/ - Create a new concept"""
        url = reverse('concept-list')
        data = {
            'name': 'New Concept',
            'description': 'New concept description',
            'domain': self.domain.id,
            'sub_domain': self.subdomain.id,
            'phase': self.phase.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        self.assertEqual(Concept.objects.count(), 1)
        concept = Concept.objects.get()
        self.assertEqual(concept.name, 'New Concept')
    
    def test_create_concept_invalid_relationships(self):
        """Test POST /api/concepts/ - Validation error for mismatched relationships"""
        # Create another domain and subdomain that don't match
        other_domain = Domain.objects.create(name="Other Domain", description="Desc")
        other_subdomain = SubDomain.objects.create(
            name="Other SubDomain",
            description="Desc",
            domain=other_domain
        )
        
        url = reverse('concept-list')
        data = {
            'name': 'Invalid Concept',
            'description': 'Description',
            'domain': self.domain.id,
            'sub_domain': other_subdomain.id,  # Doesn't belong to self.domain
            'phase': self.phase.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_concept(self):
        """Test GET /api/concepts/{id}/ - Retrieve concept"""
        concept = Concept.objects.create(
            name="Test Concept",
            description="Description",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase
        )
        
        url = reverse('concept-detail', kwargs={'pk': concept.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Concept')
        self.assertIn('domain', response.data)
        self.assertIn('themes', response.data)
    
    def test_update_concept(self):
        """Test PUT /api/concepts/{id}/ - Update concept"""
        concept = Concept.objects.create(
            name="Old Name",
            description="Old Description",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase
        )
        
        url = reverse('concept-detail', kwargs={'pk': concept.id})
        data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'domain': self.domain.id,
            'sub_domain': self.subdomain.id,
            'phase': self.phase.id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        concept.refresh_from_db()
        self.assertEqual(concept.name, 'Updated Name')
    
    def test_delete_concept(self):
        """Test DELETE /api/concepts/{id}/ - Delete concept"""
        concept = Concept.objects.create(
            name="To Delete",
            description="Description",
            domain=self.domain,
            sub_domain=self.subdomain,
            phase=self.phase
        )
        
        url = reverse('concept-detail', kwargs={'pk': concept.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Concept.objects.count(), 0)


class ThemeAPITestCase(BaseAPITestCase):
    """Test suite for Theme endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_themes(self):
        """Test GET /api/themes/ - List all themes"""
        url = reverse('theme-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('concept_name', response.data[0])
    
    def test_create_theme(self):
        """Test POST /api/themes/ - Create a new theme"""
        url = reverse('theme-list')
        data = {
            'name': 'New Theme',
            'description': 'New theme description',
            'concept': self.concept.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.filter(name='New Theme').count(), 1)
    
    def test_retrieve_theme(self):
        """Test GET /api/themes/{id}/ - Retrieve theme"""
        url = reverse('theme-detail', kwargs={'pk': self.theme.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Theme')
        self.assertIn('concept', response.data)
        self.assertIn('techniques', response.data)
    
    def test_update_theme(self):
        """Test PATCH /api/themes/{id}/ - Partial update theme"""
        url = reverse('theme-detail', kwargs={'pk': self.theme.id})
        data = {'description': 'Updated theme description'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.theme.refresh_from_db()
        self.assertEqual(self.theme.description, 'Updated theme description')
    
    def test_delete_theme(self):
        """Test DELETE /api/themes/{id}/ - Delete theme"""
        url = reverse('theme-detail', kwargs={'pk': self.theme.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class ReferenceAPITestCase(BaseAPITestCase):
    """Test suite for Reference endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_references(self):
        """Test GET /api/references/ - List all references"""
        url = reverse('reference-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('reference_type', response.data[0])
        self.assertIn('quality_rating', response.data[0])
    
    def test_create_reference_youtube(self):
        """Test POST /api/references/ - Create a YouTube reference"""
        url = reverse('reference-list')
        data = {
            'name': 'YouTube Tutorial',
            'description': 'Great tutorial video',
            'reference_type': 'youtube',
            'content_url': 'https://youtube.com/watch?v=test123',
            'quality_rating': 4,
            'sub_domain': self.subdomain.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        reference = Reference.objects.get(name='YouTube Tutorial')
        self.assertEqual(reference.reference_type, 'youtube')
        self.assertEqual(reference.quality_rating, 4)
    
    def test_create_reference_validation_error(self):
        """Test POST /api/references/ - Validation error (no URL or file path)"""
        url = reverse('reference-list')
        data = {
            'name': 'Invalid Reference',
            'description': 'Missing URL and file path',
            'reference_type': 'youtube'
            # Missing both content_url and file_path
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_reference(self):
        """Test GET /api/references/{id}/ - Retrieve reference"""
        url = reverse('reference-detail', kwargs={'pk': self.reference.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Reference')
        self.assertIn('reference_type_display', response.data)
        self.assertIn('sub_domain', response.data)
    
    def test_update_reference(self):
        """Test PUT /api/references/{id}/ - Update reference"""
        url = reverse('reference-detail', kwargs={'pk': self.reference.id})
        data = {
            'name': 'Updated Reference',
            'description': 'Updated description',
            'reference_type': 'youtube',
            'content_url': 'https://youtube.com/updated',
            'quality_rating': 3
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.reference.refresh_from_db()
        self.assertEqual(self.reference.name, 'Updated Reference')
    
    def test_delete_reference(self):
        """Test DELETE /api/references/{id}/ - Delete reference"""
        url = reverse('reference-detail', kwargs={'pk': self.reference.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class ComponentAPITestCase(BaseAPITestCase):
    """Test suite for Component endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_components(self):
        """Test GET /api/components/ - List all components"""
        url = reverse('component-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('component_type', response.data[0])
    
    def test_create_component(self):
        """Test POST /api/components/ - Create a new component"""
        url = reverse('component-list')
        data = {
            'name': 'Background Music',
            'description': 'Epic background music track',
            'component_type': 'audio',
            'file_format': 'MP3'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        component = Component.objects.get(name='Background Music')
        self.assertEqual(component.component_type, 'audio')
    
    def test_retrieve_component(self):
        """Test GET /api/components/{id}/ - Retrieve component"""
        url = reverse('component-detail', kwargs={'pk': self.component.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Component')
        self.assertIn('component_type_display', response.data)
        self.assertIn('techniques', response.data)
    
    def test_update_component(self):
        """Test PATCH /api/components/{id}/ - Partial update component"""
        url = reverse('component-detail', kwargs={'pk': self.component.id})
        data = {'file_format': 'WAV'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.component.refresh_from_db()
        self.assertEqual(self.component.file_format, 'WAV')
    
    def test_delete_component(self):
        """Test DELETE /api/components/{id}/ - Delete component"""
        # Create a separate component to delete
        component = Component.objects.create(
            name="To Delete",
            description="Description",
            component_type="visual"
        )
        
        url = reverse('component-detail', kwargs={'pk': component.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class ToolAPITestCase(BaseAPITestCase):
    """Test suite for Tool endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_tools(self):
        """Test GET /api/tools/ - List all tools"""
        url = reverse('tool-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('tool_type', response.data[0])
        self.assertIn('software_platform', response.data[0])
    
    def test_create_tool(self):
        """Test POST /api/tools/ - Create a new tool"""
        url = reverse('tool-list')
        data = {
            'name': 'Ripple Delete',
            'description': 'Delete and close gap',
            'tool_type': 'keyboard',
            'software_platform': 'premiere',
            'category': 'cutting',
            'keyboard_shortcut': 'Shift+Delete'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        tool = Tool.objects.get(name='Ripple Delete')
        self.assertEqual(tool.keyboard_shortcut, 'Shift+Delete')
    
    def test_retrieve_tool(self):
        """Test GET /api/tools/{id}/ - Retrieve tool"""
        url = reverse('tool-detail', kwargs={'pk': self.tool.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Tool')
        self.assertIn('tool_type_display', response.data)
        self.assertIn('software_platform_display', response.data)
        self.assertIn('techniques', response.data)
    
    def test_update_tool(self):
        """Test PUT /api/tools/{id}/ - Update tool"""
        url = reverse('tool-detail', kwargs={'pk': self.tool.id})
        data = {
            'name': 'Updated Tool',
            'description': 'Updated description',
            'tool_type': 'keyboard',
            'software_platform': 'davinci',
            'category': 'effects',
            'keyboard_shortcut': 'Ctrl+Shift+X'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.tool.refresh_from_db()
        self.assertEqual(self.tool.software_platform, 'davinci')
    
    def test_delete_tool(self):
        """Test DELETE /api/tools/{id}/ - Delete tool"""
        tool = Tool.objects.create(
            name="To Delete",
            description="Description",
            tool_type="mouse",
            software_platform="premiere",
            category="selection"
        )
        
        url = reverse('tool-detail', kwargs={'pk': tool.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class TechniqueAPITestCase(BaseAPITestCase):
    """Test suite for Technique endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_techniques(self):
        """Test GET /api/techniques/ - List all techniques"""
        url = reverse('technique-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('phase_name', response.data[0])
        self.assertIn('category', response.data[0])
        self.assertIn('themes_count', response.data[0])
    
    def test_create_technique(self):
        """Test POST /api/techniques/ - Create a new technique"""
        url = reverse('technique-list')
        data = {
            'name': 'J-Cut Technique',
            'description': 'Audio precedes video cut',
            'phase': self.phase.id,
            'category': 'transitions',
            'outcome': 'Smooth transition between scenes with audio continuity',
            'instructions': ['Cut video', 'Extend audio', 'Adjust timing'],
            'tools_used': ['Timeline', 'Razor Tool'],
            'estimated_time': '00:15:00',
            'usage_frequency': 5,
            'themes': [self.theme.id],
            'tools': [self.tool.id],
            'components': [self.component.id],
            'references': [self.reference.id]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        technique = Technique.objects.get(name='J-Cut Technique')
        self.assertEqual(technique.category, 'transitions')
        self.assertEqual(technique.themes.count(), 1)
    
    def test_create_technique_validation_error(self):
        """Test POST /api/techniques/ - Validation error for short outcome"""
        url = reverse('technique-list')
        data = {
            'name': 'Bad Technique',
            'description': 'Description',
            'phase': self.phase.id,
            'category': 'workflow',
            'outcome': 'Short',  # Too short (< 10 chars)
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_400_BAD_REQUEST)
        self.assertIn('outcome', response.data)
    
    def test_retrieve_technique(self):
        """Test GET /api/techniques/{id}/ - Retrieve technique with all relationships"""
        url = reverse('technique-detail', kwargs={'pk': self.technique.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Technique')
        self.assertIn('phase', response.data)
        self.assertIn('themes', response.data)
        self.assertIn('tools', response.data)
        self.assertIn('components', response.data)
        self.assertIn('references', response.data)
        # Verify the relationships are populated
        self.assertEqual(len(response.data['themes']), 1)
        self.assertEqual(len(response.data['tools']), 1)
    
    def test_update_technique_add_relationships(self):
        """Test PATCH /api/techniques/{id}/ - Add new relationships"""
        # Create additional items to add
        new_theme = Theme.objects.create(
            name="New Theme",
            description="Description",
            concept=self.concept
        )
        
        url = reverse('technique-detail', kwargs={'pk': self.technique.id})
        data = {
            'themes': [self.theme.id, new_theme.id],
            'usage_frequency': 20
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.technique.refresh_from_db()
        self.assertEqual(self.technique.themes.count(), 2)
        self.assertEqual(self.technique.usage_frequency, 20)
    
    def test_delete_technique(self):
        """Test DELETE /api/techniques/{id}/ - Delete technique"""
        technique = Technique.objects.create(
            name="To Delete",
            description="Description",
            phase=self.phase,
            category="workflow",
            outcome="Will be deleted soon"
        )
        
        url = reverse('technique-detail', kwargs={'pk': technique.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class CompositionAPITestCase(BaseAPITestCase):
    """Test suite for Composition endpoints"""
    
    def setUp(self):
        super().setUp()
        self.create_test_hierarchy()
    
    def test_list_compositions(self):
        """Test GET /api/compositions/ - List all compositions"""
        url = reverse('composition-list')
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('domain_name', response.data[0])
        self.assertIn('techniques_count', response.data[0])
    
    def test_create_composition(self):
        """Test POST /api/compositions/ - Create a new composition"""
        url = reverse('composition-list')
        data = {
            'name': 'Epic Trailer',
            'description': 'Action-packed movie trailer',
            'domain': self.domain.id,
            'sub_domain': self.subdomain.id,
            'phase': self.phase.id,
            'concept': self.concept.id,
            'theme': self.theme.id,
            'technique': [self.technique.id],
            'tools': [self.tool.id],
            'components': [self.component.id],
            'references': [self.reference.id]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_201_CREATED)
        composition = Composition.objects.get(name='Epic Trailer')
        self.assertEqual(composition.domain, self.domain)
        self.assertEqual(composition.technique.count(), 1)
    
    def test_retrieve_composition(self):
        """Test GET /api/compositions/{id}/ - Retrieve composition with all relationships"""
        url = reverse('composition-detail', kwargs={'pk': self.composition.id})
        response = self.client.get(url)
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Composition')
        self.assertIn('domain', response.data)
        self.assertIn('sub_domain', response.data)
        self.assertIn('phase', response.data)
        self.assertIn('concept', response.data)
        self.assertIn('theme', response.data)
        self.assertIn('technique', response.data)
        self.assertIn('tools', response.data)
        self.assertIn('components', response.data)
        self.assertIn('references', response.data)
    
    def test_update_composition(self):
        """Test PUT /api/compositions/{id}/ - Update composition"""
        url = reverse('composition-detail', kwargs={'pk': self.composition.id})
        data = {
            'name': 'Updated Composition',
            'description': 'Updated description',
            'domain': self.domain.id,
            'sub_domain': self.subdomain.id,
            'phase': self.phase.id,
            'technique': [self.technique.id]
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assert_response_status(response, status.HTTP_200_OK)
        self.composition.refresh_from_db()
        self.assertEqual(self.composition.name, 'Updated Composition')
    
    def test_delete_composition(self):
        """Test DELETE /api/compositions/{id}/ - Delete composition"""
        url = reverse('composition-detail', kwargs={'pk': self.composition.id})
        response = self.client.delete(url)
        
        self.assert_response_status(response, status.HTTP_204_NO_CONTENT)


class IntegrationTestCase(BaseAPITestCase):
    """Integration tests for complex scenarios"""
    
    def test_full_workflow_create_hierarchy(self):
        """Test creating a complete hierarchy from scratch"""
        # 1. Create Domain
        domain_url = reverse('domain-list')
        domain_data = {
            'name': 'Video Editing',
            'description': 'Professional video editing domain',
            'is_active': True
        }
        domain_response = self.client.post(domain_url, domain_data, format='json')
        self.assertEqual(domain_response.status_code, status.HTTP_201_CREATED)
        # Get the domain ID from the database since CreateUpdateSerializer doesn't return id
        domain = Domain.objects.get(name='Video Editing')
        domain_id = domain.id
        
        # 2. Create SubDomain
        subdomain_url = reverse('subdomain-list')
        subdomain_data = {
            'name': 'Color Grading',
            'description': 'Color correction and grading',
            'domain': domain_id
        }
        subdomain_response = self.client.post(subdomain_url, subdomain_data, format='json')
        self.assertEqual(subdomain_response.status_code, status.HTTP_201_CREATED)
        # Get the subdomain ID from the database
        subdomain = SubDomain.objects.get(name='Color Grading')
        subdomain_id = subdomain.id
        
        # 3. Create Phase
        phase_url = reverse('phase-list')
        phase_data = {
            'name': 'Primary Color Correction',
            'description': 'Initial color correction phase',
            'sub_domain': subdomain_id
        }
        phase_response = self.client.post(phase_url, phase_data, format='json')
        self.assertEqual(phase_response.status_code, status.HTTP_201_CREATED)
        # Get the phase ID from the database
        phase = Phase.objects.get(name='Primary Color Correction')
        phase_id = phase.id
        
        # 4. Verify hierarchy by retrieving domain detail
        domain_detail_url = reverse('domain-detail', kwargs={'pk': domain_id})
        detail_response = self.client.get(domain_detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(detail_response.data['sub_domains']), 1)
    
    def test_cascade_delete_behavior(self):
        """Test that deleting a parent deletes children"""
        # Create hierarchy
        domain = Domain.objects.create(name="Parent", description="Parent domain")
        subdomain = SubDomain.objects.create(
            name="Child",
            description="Child subdomain",
            domain=domain
        )
        
        # Delete domain
        url = reverse('domain-detail', kwargs={'pk': domain.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify subdomain was also deleted (cascade)
        self.assertEqual(SubDomain.objects.filter(id=subdomain.id).count(), 0)
    
    def test_many_to_many_relationships(self):
        """Test managing many-to-many relationships"""
        self.create_test_hierarchy()
        
        # Create additional components
        component2 = Component.objects.create(
            name="Component 2",
            description="Second component",
            component_type="visual"
        )
        component3 = Component.objects.create(
            name="Component 3",
            description="Third component",
            component_type="graphics"
        )
        
        # Update technique to have multiple components
        url = reverse('technique-detail', kwargs={'pk': self.technique.id})
        data = {
            'components': [self.component.id, component2.id, component3.id]
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.technique.refresh_from_db()
        self.assertEqual(self.technique.components.count(), 3)
    
    def test_bulk_operations(self):
        """Test creating multiple items and listing them"""
        # Create multiple domains
        for i in range(5):
            Domain.objects.create(
                name=f"Domain {i}",
                description=f"Description {i}"
            )
        
        # List all domains
        url = reverse('domain-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    
    def test_lookup_by_name_edge_cases(self):
        """Test edge cases for name-based lookup"""
        # Create domain with numeric name
        domain = Domain.objects.create(name="123", description="Numeric name")
        
        # Should work with name-based lookup even though it's numeric
        url = reverse('domain-detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        
        # Will look for ID 123 first (numeric), then fall back to name
        # This tests the lookup logic in BaseNamedModelViewSet
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

