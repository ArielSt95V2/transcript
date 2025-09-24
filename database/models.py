from django.db import models

class BaseModel(models.Model):
    """
    Base template for a Django model with __str__ and Meta class.
    Can be used as a starting point for most models.
    """

    # Common fields
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Example __str__ method
    def __str__(self):
        """
        Returns a human-readable representation of the object.
        By default, shows the model name and its primary key.
        Override this in child models if needed.
        """
        return f"{self.__class__.__name__} ({self.pk})"

    class Meta:
        """
        Meta class for common model configuration.
        """
        abstract = True               # Makes this a base class, no DB table created
        ordering = ['-created_at']    # Default ordering for QuerySets
        verbose_name = "Base Model"   # Human-readable singular name
        verbose_name_plural = "Base Models"  # Human-readable plural name

class Topic(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

class InformationSource(BaseModel):
    SOURCE_TYPES = [
        ('youtube', 'YouTube'),
        ('social', 'social'),
        ('manual', 'Manual'),
        ('web', 'Web Doc'),
        ('spreadsheet', 'Spreadsheet'),
        ('file', 'User Uploaded File'),
    ]

    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    source_identifier = models.CharField(max_length=255)  # e.g., video ID, URL, filename
    raw_content = models.TextField(blank=True, null=True)  # raw transcript/text
    processed_content = models.JSONField(blank=True, null=True)  # NLP-extracted info
    class Meta:
        verbose_name = "Information Source"
        verbose_name_plural = "Information Sources"

class UserQuestion(BaseModel):
    question_text = models.TextField()
    answer_text = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "User Question"
        verbose_name_plural = "User Questions"

class KnowledgeNode(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content_source = models.ForeignKey(InformationSource, on_delete=models.CASCADE)
    concept_name = models.CharField(max_length=255)  # Removed required=True
    related_nodes = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        verbose_name = "Knowledge Node"
        verbose_name_plural = "Knowledge Nodes"



