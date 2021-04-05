from django.forms import ModelForm
from .models import Animales
from django import forms


class AnimalForm(ModelForm):
    class Meta:
        model = Animales
        fields = ['especie', 'nombre', 'numero', 'comida', 'user_id']
        ANIMALES_CHOICES = (
            ("", ""),
            ("Perro", "Perro"),
            ("Cocodrilo", "Cocodrilo"),
            ("Gato", "Gato")
        )
        widgets = {
            'especie': forms.Select(
                choices=ANIMALES_CHOICES,
            ),
            'nombre': forms.TextInput(
                attrs={'size': '10'}
            ),
            'numero': forms.NumberInput(
                attrs={'style': 'width:6ch', 'min': '1'}
            ),
            'comida': forms.NumberInput(
                attrs={'style': 'width:6ch', 'value': '1', 'min': '1', 'max': '1'}
            ),
            'user_id': forms.NumberInput(
                attrs={'style': 'width:6ch', 'value': '1000'}  # dummy value 1000 is
                # replaced by user_id
            )
        }
