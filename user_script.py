import os
import django
from django.contrib.auth import get_user_model 

# Remplace 'prosui.settings' par le chemin vers ton fichier settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prosui.settings')

# Initialise Django
django.setup()


User = get_user_model()
user = User.objects.create_user(username='youcef.ely', 
                                email='youcef.lyousfi@example.com', 
                                password='S3cret!', 
                                role='supervisor')  

