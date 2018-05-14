from django import forms
    
class UploadFileForm(forms.Form):
    SOILS_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    
    delineation_file = forms.FileField()
    coverage_file = forms.FileField()
    soils = forms.ChoiceField(choices = SOILS_CHOICES)