# gestion/forms.py
from django import forms
from decimal import Decimal

# Opciones de Rastrojo con valores C/N aproximados para la lógica de cálculo
RASTROJO_CHOICES = [
    ('ninguno', 'Ninguno (Solo pulpa de café)'),
    ('maiz', 'Rastrojo de Maíz'),
    ('frijol', 'Rastrojo de Frijol'),
    ('sorgo', 'Rastrojo de Sorgo'),
]

# Formulario para la Pantalla "Nueva Mezcla"
class MezclaForm(forms.Form):
    # La capacidad máxima del tanque IBC (en litros) para determinar el agua necesaria
    CAPACIDAD_IBC_L = Decimal(1000)

    # Campos de entrada del usuario
    pulpa_cafe_kg = forms.DecimalField(
        label='Pulpa de Café (kg)',
        min_value=1, 
        initial=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rastrojo_tipo = forms.ChoiceField(
        label='Tipo de Rastrojo/Residuo',
        choices=RASTROJO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    rastrojo_kg = forms.DecimalField(
        label='Cantidad de Rastrojo (kg)', 
        min_value=0, 
        initial=20,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # Campo de salida para mostrar los litros de agua calculados
    agua_litros_necesarios = forms.DecimalField(
        label='Agua Requerida (L)',
        required=False, # No requerido en el POST, se calculará
        initial=500, # Valor inicial por defecto (será sobrescrito)
        # Hacemos que se vea como un campo, pero que esté deshabilitado para edición
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

# Formulario para la Pantalla "Monitoreo"
class MonitoreoForm(forms.Form):
    # Restricción de 1 a 14
    ph = forms.DecimalField(
        label='pH medido', 
        min_value=1.0, 
        max_value=14.0, # Límite superior
        initial=7.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    temperatura_ambiente = forms.DecimalField(
        label='Temperatura Ambiente (°C)', 
        initial=25.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )