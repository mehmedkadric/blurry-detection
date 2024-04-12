from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['threshold'].initial = 100  # Set default value for threshold

    class Meta:
        model = UploadedImage
        fields = ['image', 'threshold']
