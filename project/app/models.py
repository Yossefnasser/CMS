from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with roles for clinic staff"""
    class UserType(models.TextChoices):
        MANAGER = 'MANAGER', 'Manager'
        ADMIN = 'ADMIN', 'Admin'
        SECRETARY = 'SECRETARY', 'Secretary'
        DOCTOR = 'DOCTOR', 'Doctor'
    
    # Remove username field and use email instead
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)
    fullname = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.SECRETARY
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"


class Patient(models.Model):
    """Patient information model"""
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Clinic(models.Model):
    """Medical departments/clinics"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DoctorSchedule(models.Model):
    """Doctor availability schedule"""
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.DOCTOR}
    )
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


class Appointment(models.Model):
    """Patient appointment records"""
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserType.DOCTOR}
    )
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


class Invoice(models.Model):
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