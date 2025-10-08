# Backend Feature Workflow Template

This document provides a comprehensive workflow template for creating new backend features in this Django REST Framework project, documenting coding standards and step-by-step implementation process.

## Identified Coding Standards

### 1. Model Standards (`models.py`)

- **Inheritance**: All models inherit from `BaseModel` abstract class
- **Common fields**: name, description, created_at, updated_at (inherited)
- **String representation**: Define `__str__()` returning meaningful identifier
- **Meta class**: Include `verbose_name`, optionally `ordering`
- **Relationships**:
  - ForeignKey: Always specify `related_name`, `on_delete=models.CASCADE`
  - ManyToManyField: Use `blank=True`, specify `related_name`
- **Optional fields**: Use `blank=True, null=True`
- **Choices**: Define as lists/tuples within the model class

**Example pattern**:
```python
class NewModel(BaseModel):
    related_field = models.ForeignKey(OtherModel, on_delete=models.CASCADE, related_name='new_models')
    choice_field = models.CharField(max_length=20, choices=CHOICES)
    optional_field = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.related_field.name})"
    
    class Meta:
        verbose_name = "New Model"
        ordering = ['name']
```

### 2. Serializer Standards (`serializers.py`)

- **Three serializers per model**:
  1. `{Model}ListSerializer` - lightweight, includes counts via SerializerMethodField
  2. `{Model}DetailSerializer` - full data with nested List serializers
  3. `{Model}CreateUpdateSerializer` - for create/update operations

- **Inheritance**: All inherit from `BaseModelSerializer`
- **Read-only fields**: Always include `['id', 'created_at', 'updated_at']`
- **Validation**: 
  - `validate_name()`: minimum 2 characters, strip whitespace
  - `validate()`: cross-field validation
- **Nested data**: Use List serializers to avoid deep nesting
- **Display fields**: Use `source='get_field_display'` for choice fields

**Example patterns**:

```python
# 1. List Serializer
class NewModelListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    related_name = serializers.CharField(source='related_field.name', read_only=True)
    choice_display = serializers.CharField(source='get_choice_field_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = NewModel
        fields = ['id', 'name', 'description', 'related_name', 'choice_field', 'choice_display', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.items.count()

# 2. Detail Serializer
class NewModelDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    related_field = RelatedModelListSerializer(read_only=True)
    choice_display = serializers.CharField(source='get_choice_field_display', read_only=True)
    items = ItemListSerializer(many=True, read_only=True)
    
    class Meta:
        model = NewModel
        fields = ['id', 'name', 'description', 'related_field', 'choice_field', 'choice_display', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# 3. CreateUpdate Serializer
class NewModelCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating"""
    class Meta:
        model = NewModel
        fields = ['id', 'name', 'description', 'related_field', 'choice_field']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()
    
    def validate(self, data):
        # Cross-field validation
        if data.get('related_field') and data.get('choice_field'):
            # Validate relationships
            pass
        return data
```

### 3. ViewSet Standards (`views.py`)

- **Inheritance**: All viewsets inherit from `BaseNamedModelViewSet`
- **Required attributes**:
  - `queryset = Model.objects.all()`
  - `list_serializer_class`
  - `detail_serializer_class`
  - `create_update_serializer_class`
- **Filtering**: Override `get_queryset()` for query parameter filtering
- **Permissions**: Uses `AllowAny` (inherited from base)
- **Lookup**: Supports both ID and name lookup (inherited behavior)

**Example pattern**:
```python
class NewModelViewSet(BaseNamedModelViewSet):
    queryset = NewModel.objects.all()
    list_serializer_class = NewModelListSerializer
    detail_serializer_class = NewModelDetailSerializer
    create_update_serializer_class = NewModelCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by related field
        related_id = self.request.query_params.get('related_field')
        if related_id:
            queryset = queryset.filter(related_field_id=related_id)
        # Filter by choice field
        choice = self.request.query_params.get('choice_field')
        if choice:
            queryset = queryset.filter(choice_field=choice)
        return queryset
```

### 4. URL Standards (`urls.py`)

- Use `DefaultRouter` from rest_framework.routers
- Register with lowercase plural endpoint names
- Import all viewsets in the views import section

**Example pattern**:
```python
from .views import NewModelViewSet

router.register(r'newmodels', NewModelViewSet)
```

### 5. Migration Standards

- Auto-generated using `python manage.py makemigrations`
- Review before applying with `python manage.py migrate`

## Step-by-Step Workflow

### Step 1: Define the Model
**File**: `transcript/database/models.py`

1. Add model class inheriting from `BaseModel`
2. Define fields with appropriate types and options
3. Add ForeignKey/ManyToMany relationships with `related_name`
4. Define choice fields as class-level tuples/lists
5. Implement `__str__()` method
6. Add Meta class with `verbose_name` and optional `ordering`

### Step 2: Create Serializers
**File**: `transcript/database/serializers.py`

1. **List Serializer**:
   - Inherit from `BaseModelSerializer`
   - Add `_display` fields for choices using `source='get_field_display'`
   - Add count fields using `SerializerMethodField()`
   - Implement `get_*_count()` methods
   - Define fields in Meta (exclude nested relationships)

2. **Detail Serializer**:
   - Inherit from `BaseModelSerializer`
   - Add nested serializers (use List versions)
   - Include all related data
   - Add `_display` fields for choices
   - Define all fields in Meta

3. **CreateUpdate Serializer**:
   - Inherit from `BaseModelSerializer`
   - Include only editable fields
   - Add `validate_name()` method (min 2 chars, strip)
   - Add `validate()` for cross-field validation
   - Set `read_only_fields = ['id']`

### Step 3: Create ViewSet
**File**: `transcript/database/views.py`

1. Import model and serializers at the top
2. Create viewset class inheriting from `BaseNamedModelViewSet`
3. Set four class attributes (queryset, three serializer classes)
4. Override `get_queryset()` if filtering is needed
5. Add query parameter filters using `request.query_params.get()`

### Step 4: Register URL Routes
**File**: `transcript/database/urls.py`

1. Import the viewset in the import section
2. Register with router using lowercase plural name: `router.register(r'newmodels', NewModelViewSet)`

### Step 5: Create and Apply Migrations
**Commands**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Test Endpoints
**Available endpoints** (automatically created):
- `GET /api/newmodels/` - List all
- `POST /api/newmodels/` - Create new
- `GET /api/newmodels/{id}/` - Retrieve by ID
- `GET /api/newmodels/{name}/` - Retrieve by name
- `PUT /api/newmodels/{id}/` - Full update
- `PATCH /api/newmodels/{id}/` - Partial update
- `DELETE /api/newmodels/{id}/` - Delete

## Key Files to Modify

1. `transcript/database/models.py` - Add model
2. `transcript/database/serializers.py` - Add 3 serializers
3. `transcript/database/views.py` - Add viewset and import serializers
4. `transcript/database/urls.py` - Register route

## Best Practices

- Always use `related_name` for reverse relationships
- Keep serializers lightweight for list views
- Use SerializerMethodField for computed values
- Validate all user inputs in CreateUpdate serializers
- Add query parameter filtering in get_queryset() when needed
- Follow naming conventions: plural endpoints, PascalCase classes
- Test all CRUD operations after implementation

## Complete Example: Adding a "Category" Model

### 1. Model (models.py)
```python
class Category(BaseModel):
    CATEGORY_TYPES = [
        ('primary', 'Primary Category'),
        ('secondary', 'Secondary Category'),
        ('tag', 'Tag'),
    ]
    
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='categories')
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.domain.name})"
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['domain', 'category_type', 'name']
```

### 2. Serializers (serializers.py)
```python
class CategoryListSerializer(BaseModelSerializer):
    """Lightweight serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    category_type_display = serializers.CharField(source='get_category_type_display', read_only=True)
    subcategories_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'domain_name', 'category_type', 'category_type_display', 'is_active', 'subcategories_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_subcategories_count(self, obj):
        return obj.subcategories.count()

class CategoryDetailSerializer(BaseModelSerializer):
    """Full serializer for detail views"""
    domain = DomainListSerializer(read_only=True)
    category_type_display = serializers.CharField(source='get_category_type_display', read_only=True)
    parent_category = CategoryListSerializer(read_only=True)
    subcategories = CategoryListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'domain', 'category_type', 'category_type_display', 'parent_category', 'subcategories', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CategoryCreateUpdateSerializer(BaseModelSerializer):
    """Serializer for creating/updating categories"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'domain', 'category_type', 'parent_category', 'is_active']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Category name must be at least 2 characters long")
        return value.strip()
    
    def validate(self, data):
        # Prevent circular parent-child relationships
        parent = data.get('parent_category')
        if parent and self.instance:
            if parent.id == self.instance.id:
                raise serializers.ValidationError("A category cannot be its own parent")
        return data
```

### 3. ViewSet (views.py)
```python
# Add to imports at top
from .models import Category
from .serializers import CategoryListSerializer, CategoryDetailSerializer, CategoryCreateUpdateSerializer

# Add viewset
class CategoryViewSet(BaseNamedModelViewSet):
    queryset = Category.objects.all()
    list_serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    create_update_serializer_class = CategoryCreateUpdateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by domain
        domain_id = self.request.query_params.get('domain')
        if domain_id:
            queryset = queryset.filter(domain_id=domain_id)
        # Filter by category_type
        category_type = self.request.query_params.get('category_type')
        if category_type:
            queryset = queryset.filter(category_type=category_type)
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
```

### 4. URLs (urls.py)
```python
# Add to imports
from .views import CategoryViewSet

# Add to router
router.register(r'categories', CategoryViewSet)
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Test the API
```bash
# List categories
curl http://localhost:8000/api/categories/

# Filter by domain
curl http://localhost:8000/api/categories/?domain=1

# Create category
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Category", "description": "Test", "domain": 1, "category_type": "primary"}'

# Get by ID
curl http://localhost:8000/api/categories/1/

# Get by name
curl http://localhost:8000/api/categories/Test%20Category/
```

## Common Patterns

### Many-to-Many Relationships
When dealing with M2M fields in CreateUpdate serializers:
```python
def create(self, validated_data):
    # Extract M2M fields
    themes = validated_data.pop('themes', [])
    tools = validated_data.pop('tools', [])
    
    # Create instance
    instance = super().create(validated_data)
    
    # Set M2M relationships
    instance.themes.set(themes)
    instance.tools.set(tools)
    
    return instance

def update(self, instance, validated_data):
    # Extract M2M fields
    themes = validated_data.pop('themes', None)
    tools = validated_data.pop('tools', None)
    
    # Update instance
    instance = super().update(instance, validated_data)
    
    # Update M2M relationships if provided
    if themes is not None:
        instance.themes.set(themes)
    if tools is not None:
        instance.tools.set(tools)
    
    return instance
```

### Custom Filtering
For complex filtering needs:
```python
def get_queryset(self):
    queryset = super().get_queryset()
    
    # Search by name
    search = self.request.query_params.get('search')
    if search:
        queryset = queryset.filter(name__icontains=search)
    
    # Date range filtering
    created_after = self.request.query_params.get('created_after')
    if created_after:
        queryset = queryset.filter(created_at__gte=created_after)
    
    return queryset
```

### Custom Actions
Add custom endpoints to viewsets:
```python
from rest_framework.decorators import action

class CategoryViewSet(BaseNamedModelViewSet):
    # ... existing code ...
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        category = self.get_object()
        category.is_active = True
        category.save()
        serializer = self.get_serializer(category)
        return Response(serializer.data)
```

