from django.core.management.base import BaseCommand
from app.models import Clinic, DaysOfWeek, ClinicSlot
from datetime import datetime, date, timedelta

class Command(BaseCommand):
    help = 'Create default slots for all clinics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clinic-id',
            type=int,
            help='Create slots for specific clinic ID only',
        )

    def handle(self, *args, **options):
        if options['clinic_id']:
            try:
                clinic = Clinic.objects.get(id=options['clinic_id'])
                self.create_slots_for_clinic(clinic)
                self.stdout.write(f"Created slots for {clinic.name}")
            except Clinic.DoesNotExist:
                self.stdout.write(f"Clinic with ID {options['clinic_id']} not found")
        else:
            clinics = Clinic.objects.filter(is_active=True)
            for clinic in clinics:
                self.create_slots_for_clinic(clinic)
                self.stdout.write(f"Created slots for {clinic.name}")

    def create_slots_for_clinic(self, clinic):
        days = DaysOfWeek.objects.all()
        
        for day in days:
            current_time = clinic.default_open_time
            
            while current_time < clinic.default_close_time:
                end_datetime = datetime.combine(date.today(), current_time) + timedelta(hours=clinic.slot_duration_hours)
                end_time = end_datetime.time()
                
                if end_time <= clinic.default_close_time:
                    slot, created = ClinicSlot.objects.get_or_create(
                        clinic=clinic,
                        day_of_week=day,
                        start_time=current_time,
                        end_time=end_time
                    )
                    if created:
                        self.stdout.write(f"  Created: {slot}")
                
                current_time = end_time