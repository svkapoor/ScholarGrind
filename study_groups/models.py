from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class StudyGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    specific_room = models.CharField(max_length=100, blank=True)  # optional
    max_members = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, blank=True, related_name='study_groups')


    def __str__(self):
        return self.name
