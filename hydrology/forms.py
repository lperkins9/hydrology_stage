from django import forms
    
class UploadFileForm(forms.Form):
    delineation_file = forms.FileField()
    coverage_file = forms.FileField()