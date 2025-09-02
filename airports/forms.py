from django import forms

#  Validaciones adicionales para los códigos IATA

class AirportDistanceForm(forms.Form):
    aeropuerto_origen = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={ # Atributos HTML para el input
            'class': 'form-control',
            'placeholder': 'Ej: BOG',
            'pattern': '[A-Z]{3}',
            'title': 'Ingrese código IATA de 3 letras'
        }),
        label='Aeropuerto de Origen (Código IATA)'
    )
    
    aeropuerto_destino = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: MEX',
            'pattern': '[A-Z]{3}',
            'title': 'Ingrese código IATA de 3 letras'
        }),
        label='Aeropuerto de Destino (Código IATA)'
    )

    def clean_aeropuerto_origen(self): # Validar que el código contenga solo letras
        codigo = self.cleaned_data['aeropuerto_origen'].upper()
        if not codigo.isalpha(): # Solo letras
            raise forms.ValidationError("El código debe contener solo letras.")
        return codigo

    def clean_aeropuerto_destino(self): # Validar que el código contenga solo letras
        codigo = self.cleaned_data['aeropuerto_destino'].upper()
        if not codigo.isalpha(): # Solo letras
            raise forms.ValidationError("El código debe contener solo letras.")
        return codigo
