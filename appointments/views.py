from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime  # Importando datetime para manipulação de datas

@login_required
def schedule_appointment(request):
    # Buscar todos os horários que ainda não foram reservados
    appointments = Appointment.objects.filter(is_booked=False)

    if request.method == "POST":
        # Obter a data e hora do agendamento escolhido pelo cliente
        appointment_date = request.POST.get("date")

        # Tentar encontrar o agendamento correspondente
        try:
            appointment = Appointment.objects.get(time_slot=appointment_date)
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Agendamento não encontrado. Por favor, tente novamente.'})

        # Verificar se o agendamento já está reservado
        if appointment.is_booked:
            return JsonResponse({'status': 'error', 'message': 'Este agendamento já está reservado.'})

        # Atualizar os dados do agendamento com o cliente e marcar como reservado
        appointment.client = request.user
        appointment.is_booked = True
        appointment.save()

        return JsonResponse({'status': 'success'})

    # Exibir a página de agendamentos disponíveis
    return render(request, "appointments/schedule.html", {"appointments": appointments})

@login_required
def get_events(request):
    try:
        # Buscando todos os agendamentos no banco de dados
        appointments = Appointment.objects.all()
        
        # Criando a lista de eventos a partir dos agendamentos
        events = []
        for appointment in appointments:
            events.append({
                'title': appointment.title,  # Certifique-se de que o modelo Appointment tem um campo 'title'
                'start': appointment.start_time.isoformat()  # Certifique-se de que o modelo Appointment tem um campo 'start_time'
            })
        
        return JsonResponse(events, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_available_time_slots(request):
    date_str = request.GET.get('date')
    
    # Verifique se a data foi passada e converta-a
    if date_str:
        selected_date = datetime.fromisoformat(date_str).date()  # Converter a string para uma data
        # Filtrar horários que não estão reservados nesse dia
        appointments = Appointment.objects.filter(time_slot__date=selected_date, is_booked=False)
        available_slots = [{'time': appointment.time_slot.isoformat()} for appointment in appointments]
        return JsonResponse({'slots': available_slots})
    
    return JsonResponse({'slots': []})  # Retorna uma lista vazia se não houver data

def appointment_success(request):
    # Redirecionar para a página de sucesso
    return redirect("appointment_success")  # Certifique-se de que a URL 'appointment_success' esteja definida
