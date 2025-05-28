from django.contrib import admin
from django import forms
from .models import CustomUser

# Register your models here.


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.role == 'supervisor':
            self.fields['supervisor'].disabled = True
            self.fields['supervisor'].queryset = CustomUser.objects.none()  # Or filter only project leaders

        # Exclude self from supervisor choices
        if self.instance.pk:
            self.fields['supervisor'].queryset = CustomUser.objects.filter(role='supervisor').exclude(pk=self.instance.pk)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ['email', 'role', 'supervisor']

