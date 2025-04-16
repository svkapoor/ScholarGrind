from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    STUDENT_TYPE_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('GR', 'Graduate'),
        ('PH', 'Ph.D.'),
        ('OT', 'Other'),
    ]

    student_type = models.CharField(max_length=2, choices=STUDENT_TYPE_CHOICES, default='UG')
    institution = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    study_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_student_type_display()})"
