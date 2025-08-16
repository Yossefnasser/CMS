from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone







class User(AbstractUser):
    class UserType(models.TextChoices):
        MANAGER   = 'MANAGER', 'Manager'
        ADMIN     = 'ADMIN', 'Admin'
        SECRETARY = 'SECRETARY', 'Secretary'

    # Keep username for login
    fullname = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.SECRETARY,
        null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['fullname']  # for createsuperuser

    def __str__(self):
        return f"{self.fullname or self.username} ({self.get_user_type_display()})"


class BaseModel(models.Model):
    added_date   = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    added_by     = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_added_by', null=True, blank=True)
    deleted_by   = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_deleted_by', null=True, blank=True)
    updated_by   = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_updated_by', null=True, blank=True)

    class Meta:
        abstract = True

class Doctor(BaseModel):
    """Doctor information model"""
    full_name = models.CharField(max_length=100)
    class Specialization(models.TextChoices):
        CARDIOLOGY = 'CARDIOLOGY', 'Cardiology'#أمراض القلب
        DERMATOLOGY = 'DERMATOLOGY', 'Dermatology' #أمراض الجلدية
        PEDIATRICS = 'PEDIATRICS', 'Pediatrics' #طب الأطفال
        ORTHOPEDICS = 'ORTHOPEDICS', 'Orthopedics' #جراحة العظام
        Gynecology = 'GYNECOLOGY', 'Gynecology' #أمراض النساء
        ENT = 'ENT', 'ENT' #أمراض الأنف والأذن والحنجرة
        Dentisitry = 'DENTISTRY', 'Dentistry' #طب الأسنان
        OPHTHALMOLOGY = 'OPHTHALMOLOGY', 'Ophthalmology' #طب العيون
        cosmatic = 'COSMETIC', 'Cosmetic' #التجميل
        GENERAL = 'GENERAL', 'General Medicine'
    
    specialization = models.CharField(
        max_length=20,
        choices=Specialization.choices,
        default=Specialization.GENERAL
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    def __str__(self):
        return f"{self.full_name} ({self.specialization}) - {self.phone_number})"

class Patient(BaseModel):
    """Patient information model"""
    full_name            = models.CharField(max_length=100)
    phone_number         = models.CharField(max_length=15)
    age                  = models.PositiveIntegerField(null=True, blank=True)
    gender               = models.CharField(max_length=10, choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other')
    ])
    notes                = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"


class Clinic(BaseModel):
    """Medical departments/clinics"""
    name            = models.CharField(max_length=50)
    description     = models.TextField(blank=True, null=True)
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class DoctorSchedule(BaseModel):
    """Doctor availability schedule"""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']

    def __str__(self):
        return f"{self.doctor} at {self.clinic} on {self.date} ({self.start_time}-{self.end_time})"


class Appointment(BaseModel):
    """Patient appointment records"""
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.time} on {self.date}"


class Invoice(BaseModel):
    """Clinic invoices"""
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    paid_before = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Generate invoice number that resets daily"""
        if not self.pk:  # Only on creation
            today_invoices = Invoice.objects.filter(
                created_at__date=self.created_at.date()
            ).count()
            self.invoice_number = today_invoices + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.appointment.patient}"