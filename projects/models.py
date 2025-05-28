import pretty_errors
from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.core.files.storage import default_storage


"""
    models.CASCADE: deletes the current object once we delete the referenced object.
    models.SET_NULL: sets the current object to NULL once we delete the referenced object.
    models

"""

class Project(models.Model):
    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
        ('cancelled', 'Cancelled'),
        ('deferred', 'Deferred'),
        ('archived', 'Archived'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects_icons/', null=True, blank=True, )
    start_date = models.DateField(validators=[MinValueValidator(date.today())])
    end_date = models.DateField(validators=[MinValueValidator(date.today())])
    client_name = models.CharField(max_length=255)

    project_leader = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name='led_projects',
        null=True,
        blank=True,
        default=None
    )

    supervisor = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        related_name='supervised_projects',
        blank=True,
        null=True,
    )


    def delete(self, *args, **kwargs):
           if self.file:
               default_storage.delete(self.image.name)
           super().delete(*args, **kwargs)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/', null=False, blank=False)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(validators=[MinValueValidator(date.today())])
    end_date = models.DateField(validators=[MinValueValidator(date.today())])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')