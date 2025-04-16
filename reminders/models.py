from django.db import models
from django.conf import settings
from django.utils import timezone

class Reminder(models.Model):
    REPEAT_CHOICES = [
        ('NONE', 'Do not repeat'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MED', 'Medium'),
        ('HIGH', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    due_date = models.DateTimeField()
    repeat = models.CharField(max_length=7, choices=REPEAT_CHOICES, default='NONE')
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='MED')
    is_completed = models.BooleanField(default=False)
    notify_before = models.IntegerField(default=15, help_text='Minutes before to send notification')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} - Due: {self.due_date}"

    @property
    def is_overdue(self):
        return not self.is_completed and self.due_date < timezone.now()

    def create_next_reminder(self):
        """Create the next reminder based on repeat settings"""
        if self.repeat == 'NONE':
            return None

        from datetime import timedelta
        new_due_date = None

        if self.repeat == 'DAILY':
            new_due_date = self.due_date + timedelta(days=1)
        elif self.repeat == 'WEEKLY':
            new_due_date = self.due_date + timedelta(weeks=1)
        elif self.repeat == 'MONTHLY':
            # Add 30 days as an approximation
            new_due_date = self.due_date + timedelta(days=30)

        if new_due_date:
            return Reminder.objects.create(
                title=self.title,
                description=self.description,
                user=self.user,
                due_date=new_due_date,
                repeat=self.repeat,
                priority=self.priority,
                notify_before=self.notify_before
            )

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('REM', 'Reminder'),
        ('TASK', 'Task Due'),
        ('GROUP', 'Group Update'),
        ('QUIZ', 'Quiz Available'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=5, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # Optional relations to different types of content
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, null=True, blank=True)
    study_task = models.ForeignKey('study_plans.StudyTask', on_delete=models.CASCADE, null=True, blank=True)
    study_group = models.ForeignKey('study_groups.StudyGroup', on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user.username}"

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
