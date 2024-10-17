from django.db import models
from django.contrib.auth.models import User
from django import forms

class Appointment(models.Model):
    barber = models.ForeignKey(User, related_name="barber_appointments", on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name="client_appointments", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.date} {self.time} - {'Booked' if self.is_booked else 'Available'}"

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['barber', 'date', 'time']  # Adicione o campo para o nome do cliente se necessário

    # Se você quiser adicionar um campo para o nome do cliente diretamente
    client_name = forms.CharField(required=False)  # Adicione este campo ao formulário