from .models import *
from django import forms


class UploadImageForm(forms.ModelForm):
     class Meta:
        model = UploadImage
        fields = ['image']