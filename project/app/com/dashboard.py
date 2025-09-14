from django.shortcuts import render
from app.models import Appointment, Doctor, Patient
from django.utils import timezone
from datetime import timedelta


def dashboard(request):
    today = timezone.now().date()
    start_of_current_month = today.replace(day=1)

    if start_of_current_month.month == 1:
        start_of_previous_month = start_of_current_month.replace(year=start_of_current_month.year - 1, month=12)
    else:
        start_of_previous_month = start_of_current_month.replace(month=start_of_current_month.month - 1)

    end_of_previous_month = start_of_current_month - timedelta(days=1)

    total_patients_count = Patient.objects.filter(deleted_date__isnull=True).count()
    patients_this_month = Patient.objects.filter(
        deleted_date__isnull=True,
        added_date__gte=start_of_current_month,
        added_date__lte=today
    ).count()

    patients_last_month = Patient.objects.filter(
        deleted_date__isnull=True,
        added_date__gte=start_of_previous_month,
        added_date__lte=end_of_previous_month
    ).count()

    if patients_last_month > 0:
        patients_growth_rate = ((patients_this_month - patients_last_month) / patients_last_month) * 100
    else:
        patients_growth_rate = 0

    total_doctors_count = Doctor.objects.filter(deleted_date__isnull=True).count()
    doctors_this_month = Doctor.objects.filter(
        deleted_date__isnull=True,
        added_date__gte=start_of_current_month,
        added_date__lte=today
    ).count()

    doctors_last_month = Doctor.objects.filter(
        deleted_date__isnull=True,
        added_date__gte=start_of_previous_month,
        added_date__lte=end_of_previous_month
    ).count()

    if doctors_last_month > 0:
        doctors_growth_rate = ((doctors_this_month - doctors_last_month) / doctors_last_month) * 100
    else:
        doctors_growth_rate = 0

    context = {
        'total_patients_count': total_patients_count,
        'patients_this_month': patients_this_month,
        'patients_last_month': patients_last_month,
        'patients_growth_rate': round(patients_growth_rate, 2),
        'total_doctors_count': total_doctors_count,
        'doctors_this_month': doctors_this_month,
        'doctors_last_month': doctors_last_month,
        'doctors_growth_rate': round(doctors_growth_rate, 2),
    }
    return render(request, 'dashboard.html', context)