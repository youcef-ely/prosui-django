import sys
from PIL import Image
from io import BytesIO
from django import forms
from .models import Project, Task
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile


User = get_user_model()

class AddProjectForm(forms.ModelForm):
    project_leader = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select()
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'client_name', 'project_leader', 'image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'project_leader': forms.Select(),
            'image': forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        supervisor = kwargs.pop('supervisor', None)
        super().__init__(*args, **kwargs)
        if supervisor:
            self.fields['project_leader'].queryset = User.objects.filter(supervisor=supervisor)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('image'):
            image = Image.open(self.cleaned_data['image'])
            output = BytesIO()

            # Resize the image (example: 300x300)
            image = image.convert("RGB")
            image.thumbnail((240, 240))

            # Save resized image to BytesIO
            image.save(output, format='JPEG', quality=85)
            output.seek(0)

            instance.image = InMemoryUploadedFile(
                output, 'ImageField', f"{self.cleaned_data['image'].name.split('.')[0]}.jpg",
                'image/jpeg', sys.getsizeof(output), None
            )

        if commit:
            instance.save()
        return instance



class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.Select(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AddDocumentForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }