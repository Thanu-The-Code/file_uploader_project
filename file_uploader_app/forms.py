# file_uploader/forms.py
from django import forms

class UploadForm(forms.Form):
    directory = forms.CharField(max_length=255)
