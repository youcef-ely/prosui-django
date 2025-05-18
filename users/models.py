import pretty_errors
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


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
    profile_photo = models.ImageField(verbose_name='Profile Photo', null=True, blank=True)

    # REQUIRED_FIELDS should NOT include 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Relationship setup
    supervisor = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'},
        related_name='project_leaders'
    )

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Génération de l'username si non défini
        if not self.username:
            if self.first_name and self.last_name:
                # Génère un username unique basé sur le prénom, nom et un hash
                base_username = f"{self.first_name.lower()}.{self.last_name.lower()}"
            else:
                # Si prénom et nom non présents, on utilise l'email
                base_username = self.email.split('@')[0]
            
            # Ajoute un suffixe unique pour éviter les doublons
            unique_suffix = get_random_string(4)  # Génère un hash de 4 caractères
            self.username = f"{base_username}.{unique_suffix}"

            # Vérification d'unicité
            while CustomUser.objects.filter(username=self.username).exists():
                unique_suffix = get_random_string(4)
                self.username = f"{base_username}.{unique_suffix}"

        # Vérification si c'est un superviseur
        if self.role == 'supervisor':
            self.supervisor = None
        
        super().save(*args, **kwargs)
