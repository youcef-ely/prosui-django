import pretty_errors
from datetime import date
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('supervisor', 'Supervisor'),
        ('project_leader', 'Project Leader'),
    )
    
    # Set the username field to 'email'
    USERNAME_FIELD = 'email'

    # Add your custom fields
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    profile_photo = models.ImageField(verbose_name='Profile Photo', 
                                      blank=True, 
                                      upload_to="profile_pictures", 
                                      default="profile_pictures/base_avatar.jpg")
    
    phone_number = models.CharField(
        null=True,
        max_length=13,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed."
            )
        ]
    )
    first_login = models.BooleanField(default=True)  

    # REQUIRED_FIELDS should NOT include 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Relationship setup
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='project_leaders'
    )

    def save(self, *args, **kwargs):
        if not self.username:
            if self.first_name and self.last_name:
                base_username = f"{self.first_name.lower()}.{self.last_name.lower()}"
            else:
                base_username = self.email.split('@')[0]
            
            
            unique_suffix = get_random_string(4)  
            self.username = f"{base_username}.{unique_suffix}"

            
            while CustomUser.objects.filter(username=self.username).exists():
                unique_suffix = get_random_string(4)
                self.username = f"{base_username}.{unique_suffix}"

        # Vérification si c'est un superviseur
        if self.role == 'supervisor':
            self.supervisor = None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email