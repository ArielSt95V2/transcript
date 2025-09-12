# models.py
# In Django, you define models and Django automatically creates the database tables for you.

from django.db import models

class Conversation(models.Model):
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: user_id VARCHAR(255) NOT NULL
    user_id = models.CharField(max_length=255)

    # SQL: title VARCHAR(255)
    title = models.CharField(max_length=255, blank=True, null=True)

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

    # SQL: updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP (updated via triggers)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    # SQL: role VARCHAR(20) NOT NULL CHECK(role IN ('user','assistant','system'))
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # SQL: content TEXT NOT NULL
    content = models.TextField()

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

class MessageFeedback(models.Model):
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: message_id INTEGER NOT NULL REFERENCES messages(id) ON DELETE CASCADE
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    # SQL: feedback_type VARCHAR(20) CHECK(feedback_type IN ('thumbs_up','thumbs_down','report'))
    FEEDBACK_CHOICES = [
        ('thumbs_up', 'Thumbs Up'),
        ('thumbs_down', 'Thumbs Down'),
        ('report', 'Report'),
    ]
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_CHOICES)

    # SQL: feedback_text TEXT
    feedback_text = models.TextField(blank=True, null=True)

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)



class Profession(models.Model):
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: name VARCHAR(100) NOT NULL UNIQUE
    name = models.CharField(max_length=100, unique=True)

    # SQL: description TEXT
    description = models.TextField(blank=True, null=True)

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ContentSource(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('youtube_transcript', 'YouTube Transcript'),
        ('scraped_website', 'Scraped Website'),
        ('uploaded_file', 'Uploaded File'),
    ]

    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: profession_id INTEGER NOT NULL REFERENCES profession(id) ON DELETE CASCADE
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='content_sources')

    # SQL: source_type VARCHAR(20) NOT NULL CHECK(source_type IN ('youtube_transcript','scraped_website','uploaded_file'))
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)

    # SQL: title VARCHAR(255) NOT NULL
    title = models.CharField(max_length=255)

    # SQL: content TEXT NOT NULL
    content = models.TextField()

    # SQL: source_url VARCHAR(...) NULL
    source_url = models.URLField(blank=True, null=True)

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

    # SQL: updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP (updated via triggers)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_source_type_display()})"

    class Meta:
        ordering = ['-created_at']

class ContentMetadata(models.Model):
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Django implicitly adds an AutoField primary key named `id`

    # SQL: content_source_id INTEGER NOT NULL REFERENCES contentsource(id) ON DELETE CASCADE
    content_source = models.ForeignKey(ContentSource, on_delete=models.CASCADE, related_name='metadata')

    # SQL: metadata_key VARCHAR(100) NOT NULL
    metadata_key = models.CharField(max_length=100)

    # SQL: metadata_value TEXT NOT NULL
    metadata_value = models.TextField()

    # SQL: created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metadata_key}: {self.metadata_value[:50]}"

    class Meta:
        unique_together = ['content_source', 'metadata_key']
        ordering = ['metadata_key']