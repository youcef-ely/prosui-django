import pretty_errors
from django.test import TestCase

# Create your tests here.
from models import User


# Liste tous les utilisateurs
for user in User.objects.all():
    print(user.email, user.role)
