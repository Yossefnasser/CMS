from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from app.helpers import get_id_hashed_of_object







class User(AbstractUser):
    class UserType(models.TextChoices):
        MANAGER   = 'MANAGER', 'Manager'
        ADMIN     = 'ADMIN', 'Admin'
        SECRETARY = 'SECRETARY', 'Secretary'

    # Keep username for login
    fullname  = models.CharField(max_length=100, null=True, blank=True)
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
        
class Specialization(BaseModel):
    """Specialization model"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Doctor(BaseModel):
    """Doctor information model"""
    full_name                = models.CharField(max_length=100)
    specialization           = models.ForeignKey(Specialization, on_delete=models.PROTECT, related_name="doctors")
    phone_number             = models.CharField(max_length=15, blank=True, null=True)
    email                    = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"
    

class Patient(BaseModel):
    """Patient information model"""
    name            = models.CharField(max_length=100)
    phone_number         = models.CharField(max_length=15)
    age                  = models.PositiveIntegerField(null=True, blank=True , default=None)
    gender               = models.CharField(max_length=10, choices=[
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ], blank=True, null=True)
    notes                = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "Patient"

    def to_json(self):
        return {
            'id'        : self.id,
            'hash_id'   : get_id_hashed_of_object(self.id),
            'name' : self.name,
            'phone_number': self.phone_number,
            'age'       : self.age,
            'gender'    : self.gender,
            'notes'     : self.notes,
        }
    
    def __str__(self):
        return f"{self.name}"


class Clinic(BaseModel):
    """Medical departments/clinics"""
    name            = models.CharField(max_length=50)
    description     = models.TextField(blank=True, null=True)
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return self.name 


class DoctorSchedule(BaseModel):
    """Doctor availability schedule"""
    doctor                 = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic                 = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date                   = models.DateField()
    start_time             = models.TimeField()
    end_time               = models.TimeField()
    is_available           = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']

    def __str__(self):
        return f"{self.doctor} at {self.clinic} on {self.date} ({self.start_time}-{self.end_time})"

class Status(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself
# DRY : Dont Repeat Yourself

class Appointment(BaseModel):
    """Patient appointment records"""

    
    patient  = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor   = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic   = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    status   = models.ForeignKey(Status, on_delete=models.CASCADE)
    date     = models.DateField()
    time     = models.TimeField()
    notes      = models.TextField(blank=True, null=True)



    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.time} on {self.date}"


class Invoice(BaseModel):
    """Clinic invoices"""
    
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    paid_before = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='invoices')
    created_at  = models.DateTimeField(auto_now_add=True)

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