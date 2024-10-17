from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('success/', views.appointment_success, name='appointment_success'),
    path('get-events/', views.get_events, name='get_events'),  # URL para eventos
]
