from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class StudyPlan(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIGH', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_plans')
    subject = models.ForeignKey('study_groups.Subject', on_delete=models.CASCADE, related_name='study_plans')
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='MED')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(is_completed=True).count()
        return (completed_tasks / total_tasks) * 100

class StudyTask(models.Model):
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    estimated_duration = models.IntegerField(
        help_text='Estimated duration in minutes',
        validators=[MinValueValidator(1)]
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'due_date']

    def __str__(self):
        return f"{self.title} ({self.study_plan.title})"

class StudySession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sessions')
    task = models.ForeignKey(StudyTask, on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(help_text='Duration in minutes', null=True, blank=True)
    notes = models.TextField(blank=True)
    productivity_rating = models.IntegerField(
        validators=[MinValueValidator(1), MinValueValidator(5)],
        null=True,
        blank=True,
        help_text='Rate your productivity from 1-5'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Study session by {self.user.username} on {self.start_time.date()}"

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds() / 60
            self.duration = round(duration)
        super().save(*args, **kwargs)
