from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Owner, Pet, Appointment, MedicalHistory
from .forms import OwnerForm, PetForm, AppointmentForm, MedicalHistoryForm

class CustomLoginView(LoginView):
    template_name = 'clinic/login.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'clinic/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(status='PENDING').order_by('date', 'time')[:5]
        return context

class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'clinic/owner_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Dueño registrado exitosamente.')
        return super().form_valid(form)

class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = 'clinic/pet_form_v2.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Mascota registrada exitosamente.')
        return super().form_valid(form)

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'clinic/appointment_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Cita agendada exitosamente.')
        return super().form_valid(form)

class MedicalHistoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'clinic/medical_history_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.groups.filter(name='Veterinario').exists() or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.veterinarian = self.request.user
        messages.success(self.request, 'Historial médico registrado exitosamente.')
        return super().form_valid(form)
