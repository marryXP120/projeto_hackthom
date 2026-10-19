from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Medicao


class CadastroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class MedicaoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        label="Data e hora",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Medicao
        fields = ["sistolica", "diastolica", "pulso", "data_hora", "observacao"]

    def clean(self):
        dados = super().clean()
        s, d = dados.get("sistolica"), dados.get("diastolica")
        if s and d and s <= d:
            raise forms.ValidationError("A sistólica deve ser maior que a diastólica.")
        return dados
