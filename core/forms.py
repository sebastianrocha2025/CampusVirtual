from django import forms
from .models import SolicitudInscripcion

class SolicitudInscripcionForm(forms.ModelForm):

    class Meta:
        model = SolicitudInscripcion
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'mensaje': forms.Textarea(attrs={'rows': 3})
        }