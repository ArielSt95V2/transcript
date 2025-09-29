from django.db import models

class BaseModel(models.Model):
    """
    Base template for a Django model with __str__ and Meta class.
    Can be used as a starting point for most models.
    """
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.__class__.__name__} ({self.pk})"

    class Meta:
        """
        Meta class for common model configuration.
        """
        abstract = True               
        ordering = ['-created_at']    
        verbose_name = "Base Model"   
        verbose_name_plural = f"{verbose_name}s"

class Domain(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # Icon identifier
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Domain"

class SubDomain(BaseModel):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='sub_domains')
    class Meta:
        verbose_name = "Sub Domain"

class Phase(BaseModel):
    sub_domain = models.ForeignKey(SubDomain, on_delete=models.CASCADE, related_name='phases')
    class Meta:
        verbose_name = "Phase"

class Concept(BaseModel):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='concepts')
    sub_domain = models.ForeignKey(SubDomain, on_delete=models.CASCADE, related_name='concepts')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='concepts')
    class Meta:
        verbose_name = "Concept"
class Theme(BaseModel):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='themes')
    class Meta:
        verbose_name = "Theme"

class Reference(BaseModel):
    """
    Case studies or illustrations - worked-out examples
    """
    REFERENCE_TYPES = [
        ('youtube', 'YouTube Link'),
        ('file_path', 'File Path'),
        ('text_segment', 'Text Segment'),
        ('image', 'Image'),
        ('audio', 'Audio Clip'),
        ('video_clip', 'Video Clip'),
        ('tutorial', 'Tutorial'),
    ]
    
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES)
    content_url = models.URLField(blank=True, null=True)  # For YouTube links
    file_path = models.CharField(max_length=500, blank=True, null=True)  # For local files
    timestamp_start = models.DurationField(null=True, blank=True)  # Start time in video
    timestamp_end = models.DurationField(null=True, blank=True)  # End time in video
    thumbnail_url = models.URLField(blank=True, null=True)  # Preview image
    quality_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    sub_domain = models.ForeignKey(SubDomain, on_delete=models.CASCADE, related_name='references', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.reference_type})"
    
    class Meta:
        verbose_name = "Reference"
        ordering = ['-quality_rating', 'name']

class Component(BaseModel):

    file_format = models.CharField(max_length=20, blank=True, null=True)  # e.g., "MP3", "MP4"
    component_type = models.CharField(
        choices=[
            ('audio', 'Audio'),
            ('visual', 'Visual'),
            ('graphics', 'Graphics'),
            ('text', 'Text/Typography'),
            ('effect', 'Effect'),
            ('transition', 'Transition'),
            ('overlay', 'Overlay'),
            ('configuration', 'Configuration'), # preset, template, plugin, extension, etc.
        ])
    
    def __str__(self):
        return f"{self.name} ({self.component_type})"
    
    class Meta:
        verbose_name = "Component"
        ordering = ['component_type', 'name']

class Tool(BaseModel):

    keyboard_shortcut = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Ctrl + C"
    tool_type = models.CharField(
        choices=[
            ('keyboard', 'Keyboard Shortcut'),
            ('mouse', 'Mouse Tool'),
            ('software_feature', 'Software Feature'),
            ('plugin', 'Plugin/Extension'),
            ('hardware', 'Hardware Tool'),
            ('command', 'Command/Tool'),
        ])
    software_platform = models.CharField(
        choices=[
            ('premiere', 'Adobe Premiere Pro'),
            ('davinci', 'DaVinci Resolve'),
            ('audition', 'Adobe Audition'),
            ('after_effects', 'After Effects'),
            ('universal', 'Universal'),
            ('multiple', 'Multiple Platforms'),
        ])
    category = models.CharField(
        choices=[
            ('cutting', 'Cutting'),
            ('trimming', 'Trimming'),
            ('effects', 'Effects'),
            ('audio', 'Audio'),
            ('navigation', 'Navigation'),
            ('selection', 'Selection'),
            ('timeline', 'Timeline'),
        ])

    def __str__(self):
        return f"{self.name} ({self.software_platform})"
    
    class Meta:
        verbose_name = "Tool"
        ordering = ['software_platform', 'category', 'name']

class Technique(BaseModel):

    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='techniques')
    themes = models.ManyToManyField(Theme, related_name='techniques', blank=True)
    tools = models.ManyToManyField(Tool, related_name='techniques', blank=True)
    components = models.ManyToManyField(Component, related_name='techniques', blank=True)
    references = models.ManyToManyField(Reference, related_name='techniques', blank=True) #Example: YouTube link → video clip → audio clip.

    category = models.CharField(
        choices=[
            ('Storytelling', 'Rhythm & timing (how editing communicates the story)'),
            ('rhythm_timing', 'Rhythm & timing (how it flows)'),
            ('transitions', 'Transitions (how shots connect)'),
            ('sound', 'Sound (what it feels like to hear)'),
            ('emotion_psychology', 'Emotion/psychology (how it makes you feel)'),
            ('visual_composition', 'Visual composition (what you look at)'),
            ('style_creativity', 'Style/creativity (what makes it unique)'),
            ('workflow', 'Workflow (how you efficiently execute)'),
            ])
    outcome = models.TextField()  #Example: Cutting to the beat → makes the trailer feel dynamic and engaging.
    instructions = models.JSONField(default=list)  #Example: Identify beats → place markers → cut clips on beats.
    tools_used = models.JSONField(default=list)  #Example: Timeline → Marker Tool → Cut Tool.
 
    estimated_time = models.DurationField(null=True, blank=True)  # How long to apply
    usage_frequency = models.IntegerField(default=0)  # Track how often it's used
    
    def __str__(self):
        return f"{self.name} ({self.phase.name})"
    
    class Meta:
        verbose_name = "Technique"
        ordering = ['phase', 'category', 'name']

class Composition(BaseModel):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='compositions', null=True, blank=True)
    sub_domain = models.ForeignKey(SubDomain, on_delete=models.CASCADE, related_name='compositions', null=True, blank=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='compositions', null=True, blank=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='compositions', null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='compositions', null=True, blank=True)
    technique = models.ManyToManyField(Technique, related_name='compositions', blank=True)
    tools = models.ManyToManyField(Tool, related_name='compositions', blank=True)
    components = models.ManyToManyField(Component, related_name='compositions', blank=True)
    references = models.ManyToManyField(Reference, related_name='compositions', blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.domain.name})"
    
    class Meta:
        verbose_name = "Composition"    