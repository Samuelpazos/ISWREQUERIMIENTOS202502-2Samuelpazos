from django import forms
from .models import Owner, Pet, Appointment, MedicalHistory
from django.core.exceptions import ValidationError

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'document', 'address', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Nombre completo'}),
            'document': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Número de documento'}),
            'address': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Dirección de residencia'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Número de teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'correo@ejemplo.com'}),
        }

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'sex', 'weight', 'health_status', 'owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Nombre de la mascota'}),
            'species': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Especie (ej. Perro, Gato)'}),
            'breed': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Raza'}),
            'age': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Edad en años'}),
            'sex': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'weight': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Peso en kg'}),
            'health_status': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': 'Estado de salud general'}),
            'owner': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason', 'veterinarian']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-2 border rounded'}),
            'reason': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Motivo de la consulta'}),
            'veterinarian': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        veterinarian = cleaned_data.get('veterinarian')

        if date and time and veterinarian:
            if Appointment.objects.filter(date=date, time=time, veterinarian=veterinarian).exists():
                raise ValidationError("Este veterinario ya tiene una cita en ese horario.")
        return cleaned_data

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['pet', 'diagnosis', 'treatment', 'allergies', 'observations']
        widgets = {
            'pet': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'diagnosis': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': 'Diagnóstico detallado'}),
            'treatment': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 3, 'placeholder': 'Plan de tratamiento'}),
            'allergies': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 2, 'placeholder': 'Alergias conocidas'}),
            'observations': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 2, 'placeholder': 'Observaciones adicionales'}),
        }
