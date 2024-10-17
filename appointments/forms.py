from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['barber', 'date', 'time']  # Adicione o campo para o nome do cliente se necessário

    # Se você quiser adicionar um campo para o nome do cliente diretamente
    client_name = forms.CharField(required=False)  # Adicione este campo ao formulário
