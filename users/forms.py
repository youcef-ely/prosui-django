# forms.py
import pretty_errors
from django import forms
from .models import CustomUser
from django.utils.safestring import mark_safe
from django.contrib.auth import password_validation
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python
from django.contrib.auth.forms import PasswordChangeForm




class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


class CompleteProfileForm(forms.ModelForm):

    username = forms.CharField(
        label='Username',
        disabled=True,
        required=False
    )
  
    email = forms.EmailField(
        label='Email',
        disabled=True,
        required=False
    )
   
    phone_number = PhoneNumberField(region="MA",
                                   widget=forms.TextInput(attrs={
                                        'placeholder': '+212 612-345678'
                                    }),
                                   required=False
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"id": "image_field"})
    )

    # Ajout des champs job et location avec leurs choix
    job = forms.ChoiceField(
        label="Job",
        choices=[('', 'Select a job')] + list(CustomUser.JOB_CHOICES),
        required=False
    )

    location = forms.ChoiceField(
        label="Location",
        choices=[('', 'Select a city')] + list(CustomUser.LOCATION_CHOICES),
        required=False
    )

    # Champs pour mot de passe
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        help_text=mark_safe('<br>'.join(password_validation.password_validators_help_texts())),
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'profile_photo',
            'job', 'location'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('instance')
        super().__init__(*args, instance=user, **kwargs)
        self.user = user
        # Initialiser les choix de job et location à partir de l'instance
        self.fields['job'].initial = user.job
        self.fields['location'].initial = user.location

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            try:
                phone_obj = to_python(phone)
                if not phone_obj.is_valid():
                    raise ValidationError("Invalid phone number.")
            except Exception:
                raise ValidationError("Invalid phone number")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password")
        pw2 = cleaned_data.get("confirm_password")

        if pw1 or pw2:
            if pw1 != pw2:
                raise ValidationError("Passwords do not match")
            if self.user.check_password(pw1):
                raise ValidationError("New password must be different from the old one.")
        else:
            raise ValidationError("You should set a new password")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        pw1 = self.cleaned_data.get("new_password")
        if pw1:
            user.set_password(pw1)
        if commit:
            user.save()
        return user
    

class UpdateProfileForm(forms.ModelForm):   

    phone_number = PhoneNumberField(
        region="MA",
        widget=forms.TextInput(attrs={'placeholder': '+212 612-345678'}),
        required=False
    )

    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"id": "image_field"})
    )

    job = forms.ChoiceField(
        label="Job",
        choices=[('', 'Select a job')] + list(CustomUser.JOB_CHOICES),
        required=False
    )

    location = forms.ChoiceField(
        label="Location",
        choices=[('', 'Select a city')] + list(CustomUser.LOCATION_CHOICES),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number',
            'profile_photo', 'job', 'location'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('instance')
        super().__init__(*args, instance=user, **kwargs)
        self.user = user
        self.fields['job'].initial = user.job
        self.fields['location'].initial = user.location

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            try:
                phone_obj = to_python(phone)
                if not phone_obj.is_valid():
                    raise ValidationError("Invalid phone number.")
            except Exception:
                raise ValidationError("Invalid phone number")
        return phone
    

class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'txtb', 'placeholder': 'Enter your old password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'txtb', 'placeholder': 'Enter your new password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'txtb', 'placeholder': 'Confirm your new password'
        })