from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ["title", "description"]
        widget = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border rounded",
                "placeholder": "Enter the movie title"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-3 py-2 border rounded",
                "placeholder": "Why should this movie be added?",
                "rows": 4
            }),
        }
        labels = {
            "title": "Movie Title",
            "description": "Description (optional)",
        }