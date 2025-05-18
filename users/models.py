from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser  

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('supervisor', 'Supervisor'),
        ('project_leader', 'Project Leader'),
    )
    role = models.fields.CharField(max_length=20, choices=ROLE_CHOICES)

    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='project_leaders'
    )

    def save(self, *args, **kwargs):
        if self.role == 'supervisor':
            self.supervisor = None
        super().save(*args, **kwargs)