import pretty_errors
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('The Email must be set')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
    
        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)
    
            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_staff=True.')
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('Superuser must have is_superuser=True.')
            return self.create_user(email, password, **extra_fields)
        

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('supervisor', 'Supervisor'),
        ('project_leader', 'Project Leader'),
    )
    
    # Liste des jobs liés à l'informatique
    JOB_CHOICES = (
        ('software_engineer', 'Software Engineer'),
        ('data_scientist', 'Data Scientist'),
        ('devops_engineer', 'DevOps Engineer'),
        ('system_administrator', 'System Administrator'),
        ('product_manager', 'Product Manager'),
        ('ui_ux_designer', 'UI/UX Designer'),
        ('qa_engineer', 'QA Engineer'),
        ('business_analyst', 'Business Analyst'),
        ('security_specialist', 'Security Specialist'),
        ('network_engineer', 'Network Engineer'),
        # tu peux en ajouter d'autres selon tes besoins
    )

    # Liste des villes marocaines
    LOCATION_CHOICES = (
        ('casablanca', 'Casablanca'),
        ('rabat', 'Rabat'),
        ('marrakech', 'Marrakech'),
        ('fes', 'Fès'),
        ('tanger', 'Tanger'),
        ('agadir', 'Agadir'),
        ('meknes', 'Meknès'),
        ('oujda', 'Oujda'),
        ('kenitra', 'Kénitra'),
        ('nador', 'Nador'),
        # Ajoute d'autres villes si besoin
    )
    
    # Set the username field to 'email'
    USERNAME_FIELD = 'email'

    # Add your custom fields
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_login_date = models.DateField(default=date.today)
    job = models.CharField(max_length=30, choices=JOB_CHOICES, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)
    first_login = models.BooleanField(default=True)  
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES, blank=True, null=True)
    profile_photo = models.ImageField(verbose_name='Profile Photo', 
                                      blank=True, 
                                      upload_to="profile_pictures", 
                                      null=True)
    

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

    objects = CustomUserManager()

    def clean(self):
        if self.role == 'supervisor' and self.supervisor is not None:
            raise ValidationError("A supervisor cannot have another supervisor.")
        if self.supervisor and self.supervisor == self:
            raise ValidationError("A user cannot be their own supervisor.")

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
