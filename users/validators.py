import pretty_errors
from django.core.exceptions import ValidationError
import re

def validate_international_phone(value):
    pattern = r'^\+\d{6,15}$'  
    if not re.match(pattern, value):
        raise ValidationError(
            "Enter a valid phone number in international format, e.g. +212623456789"
        )
    
    if len(value) > 15:
        raise ValidationError(
            "Your phone number exceeds 15 digits"
        )