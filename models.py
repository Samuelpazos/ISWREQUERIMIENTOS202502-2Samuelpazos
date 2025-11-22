from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Owner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    document = models.CharField(max_length=20, verbose_name="Documento")
    address = models.CharField(max_length=200, verbose_name="Dirección")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Dueño"
        verbose_name_plural = "Dueños"

class Pet(models.Model):
    SEX_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]
    
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets', verbose_name="Dueño")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    species = models.CharField(max_length=50, verbose_name="Especie")
    breed = models.CharField(max_length=50, verbose_name="Raza")
    age = models.PositiveIntegerField(verbose_name="Edad (años)")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Sexo")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso (kg)")
    health_status = models.TextField(verbose_name="Estado de Salud")

    class Meta:
        unique_together = ('owner', 'name')
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    def __str__(self):
        return f"{self.name} ({self.owner.name})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmada'),
        ('COMPLETED', 'Completada'),
        ('CANCELLED', 'Cancelada'),
    ]

    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    reason = models.CharField(max_length=200, verbose_name="Motivo")
    veterinarian = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Veterinario'}, related_name='appointments', verbose_name="Veterinario")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")

    class Meta:
        unique_together = ('date', 'time', 'veterinarian')
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"{self.date} {self.time} - {self.veterinarian.username}"

class MedicalHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='history', verbose_name="Mascota")
    veterinarian = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Veterinario Responsable")
    diagnosis = models.TextField(verbose_name="Diagnóstico")
    treatment = models.TextField(verbose_name="Tratamiento")
    allergies = models.TextField(blank=True, verbose_name="Alergias")
    observations = models.TextField(blank=True, verbose_name="Observaciones")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"
