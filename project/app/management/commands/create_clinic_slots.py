from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from app.models import Clinic, ClinicSlot  # 🔁 change 'app' to your actual app name

class Command(BaseCommand):
    help = "Generate 1-hour clinic slots based on each clinic's open and close times"

    def handle(self, *args, **options):
        clinics = Clinic.objects.filter(is_active=True)

        for clinic in clinics:
            self.stdout.write(self.style.WARNING(f"Creating slots for: {clinic.name}"))

            # Delete old slots
            ClinicSlot.objects.filter(clinic=clinic).delete()

            open_time = datetime.combine(datetime.today(), clinic.default_open_time)
            close_time = datetime.combine(datetime.today(), clinic.default_close_time)
            slot_duration = timedelta(hours=1)

            created = 0
            while open_time + slot_duration <= close_time:
                ClinicSlot.objects.create(
                    clinic=clinic,
                    start_time=open_time.time(),
                    end_time=(open_time + slot_duration).time(),
                    is_active=True
                )
                created += 1
                open_time += slot_duration

            self.stdout.write(self.style.SUCCESS(f"✅ Created {created} slots for {clinic.name}"))
        
        self.stdout.write(self.style.SUCCESS("🎯 All clinic slots have been generated successfully."))
