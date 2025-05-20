# forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth import password_validation
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm



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

    image = forms.ImageField()
    
    phone_number = forms.CharField(
        max_length=13,  # Adjust based on your needs
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 13 digits allowed."
            )
        ]
    )


    profile_photo = forms.ImageField(required=False)

    # Add password fields
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        required=False,
        help_text=mark_safe('<br>'.join(password_validation.password_validators_help_texts())),
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'profile_photo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('instance')
        super().__init__(*args, instance=user, **kwargs)
        self.user = user  # store user instance for password validation

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password")
        pw2 = cleaned_data.get("confirm_password")

        if pw1 or pw2:
            if pw1 != pw2:
                raise forms.ValidationError("The two password fields must match.")
            if len(pw1) < 8:
                raise forms.ValidationError("The new password must be at least 8 characters long.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        pw1 = self.cleaned_data.get("new_password1")
        if pw1:
            user.set_password(pw1)  # set new password properly

        if commit:
            user.save()
        return user
