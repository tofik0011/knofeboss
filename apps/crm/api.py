from datetime import timedelta

from django.core.checks.security import csrf
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.crm.models import Appointment, Master
from django.utils.datetime_safe import datetime


@csrf_exempt
def get_master_day_schedule(request):
    master_id = request.POST.get('master_id')
    date = request.POST.get('date')
    date = datetime.strptime(date, '%d.%m.%Y')
    master = Master.objects.get(id=master_id)
    return JsonResponse({'success': True, 'schedule': master.get_day_schedule(date)})


def add_appointment(request):
    procedure_id = request.POST.get('procedure_id', None)
    master_id = request.POST.get('master_id', None)
    client_id = request.POST.get('client_id', None)
    date = request.POST.get('date', None)
    time = request.POST.get('time', None)
    date = date.strptime(date, '%d.%m.%Y')
    time = time.strptime(time, '%H:%M')
    date_time = date + timedelta(hours=time.hour, minutes=time.date)
    print(datetime.combine(date, time))
    i = Appointment.objects.filter().exists()
    appointment = Appointment.objects.create(client_fk_id=client_id,
                                             master_fk_id=master_id,
                                             procedure_fk_id=procedure_id)


