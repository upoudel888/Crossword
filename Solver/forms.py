from django import forms
from .models import UserImages

class UserImagesForm(forms.ModelForm):
    
    class Meta:
        model = UserImages
        fields = ("img",)
    
