from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        # Darle estilos desde Django
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important' : forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
