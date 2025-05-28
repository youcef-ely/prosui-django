import pretty_errors
from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        # Optionally create test data here if you're not using a test DB already populated
        # For example:
        # supervisor = CustomUser.objects.create(email='youcef.lyousfi@gmail.com', role='supervisor', ...)
        pass

    def test_get_supervised_users(self):
        try:
            user = CustomUser.objects.get(email='youcef.lyousfi@gmail.com')
            print(user.email)
            if user is None:
                print("Admin not found.")
                return 
            users = CustomUser.objects.filter(supervisor=user)

            for u in users:
                print(u.email)
        except CustomUser.DoesNotExist:
            print("User not found.")
