from django.db import models
from django.conf import settings

class AIStudySession(models.Model):
    SESSION_TYPES = [
        ('QA', 'Question & Answer'),
        ('FLASH', 'Flashcards'),
        ('SUM', 'Text Summarization'),
        ('QUIZ', 'Quiz Generation'),
        ('NOTES', 'Note Taking'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_sessions')
    session_type = models.CharField(max_length=5, choices=SESSION_TYPES)
    subject = models.ForeignKey('study_groups.Subject', on_delete=models.CASCADE, related_name='ai_sessions')
    topic = models.CharField(max_length=200)
    content = models.TextField(help_text='Original content or question')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_session_type_display()} session by {self.user.username}"

class AIResponse(models.Model):
    session = models.ForeignKey(AIStudySession, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_rating = models.IntegerField(null=True, blank=True, help_text='User rating from 1-5')
    feedback_text = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Response in {self.session}"

class Flashcard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flashcards')
    subject = models.ForeignKey('study_groups.Subject', on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField()
    back = models.TextField()
    is_ai_generated = models.BooleanField(default=False)
    difficulty_rating = models.IntegerField(default=1, help_text='Difficulty from 1-5')
    next_review = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_review', 'created_at']

    def __str__(self):
        return f"Flashcard: {self.front[:50]}..."

class StudyMaterial(models.Model):
    MATERIAL_TYPES = [
        ('NOTE', 'Study Notes'),
        ('SUM', 'Summary'),
        ('OUT', 'Outline'),
        ('QA', 'Q&A Set'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_materials')
    subject = models.ForeignKey('study_groups.Subject', on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=200)
    content = models.TextField()
    material_type = models.CharField(max_length=4, choices=MATERIAL_TYPES)
    is_ai_generated = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_material_type_display()}: {self.title}"
