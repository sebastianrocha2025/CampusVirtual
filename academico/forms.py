from django import forms
from .models import Nota, Asistencia
from .models import Clase, Cuestionario, Pregunta, Opcion, RespuestaOpcion, MaterialClase
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['cuestionario', 'valor']

        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['fecha', 'presente']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = [ "curso","titulo","orden", "descripcion", "visible"]
class CuestionarioForm(forms.ModelForm):
    class Meta:
        model = Cuestionario
        fields = ["descripcion","titulo", "activo"]

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ["texto", "es_correcta"]


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto"]

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ["texto", "imagen", "es_correcta"]



OpcionFormSet = inlineformset_factory(
    Pregunta,
    Opcion,
    form=OpcionForm,
    extra=2,
    min_num=2,
    validate_min=True,
    can_delete=True
)