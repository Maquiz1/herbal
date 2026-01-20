from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.urls import reverse
from locations.models import Site  # Assuming you have a locations app
from . audit_model import AuditModel

class Patient(AuditModel):
    """
    Comprehensive patient demographic and enrollment tracking model.
    """

    rec_date = models.DateField(blank=True, null=True)

    # Unique identifiers
    pid = models.CharField(max_length=255, unique=True)  # Patient ID
    hid = models.CharField(max_length=255, blank=True, null=True)  # Hospital ID
    nid = models.CharField(max_length=255, blank=True, null=True)  # National ID

    # Name
    fname = models.CharField(max_length=255, blank=True, null=True)
    mname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)

    # Demographics
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, blank=True, null=True)

    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('Se', 'Separated'),
        ('W', 'Widowed/Widower'),
        ('C', 'Cohabitating'),
    )
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)

    EDUCATION_CHOICES = (
        ('1', 'Not Attended School'),
        ('2', 'Primary'),
        ('3', 'Secondary'),
        ('4', 'Certificate'),
        ('5', 'Diploma'),
        ('6', 'Undergraduate'),
        ('7', 'Postgraduate'),
    )
    education = models.CharField(max_length=25, choices=EDUCATION_CHOICES, blank=True, null=True)

    occupation = models.CharField(max_length=50, blank=True, null=True)

    # Contact
    phone_patient = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$', 'Enter a valid phone number.')]
    )
    phone_relative = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$', 'Enter a valid phone number.')]
    )

    # Address
    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    ward = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)

    # Staff & Site
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    # Status & Comments
    status = models.PositiveIntegerField(default=0)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']

    def __str__(self):
        name = f"{self.fname or ''} {self.mname or ''} {self.lname or ''}".strip()
        if name:
            return f"{name} ({self.pid or 'No ID'})"
        return self.pid or f"Patient {self.pk}"

    def get_full_name(self):
        return f"{self.fname or ''} {self.mname or ''} {self.lname or ''}".strip() or "Unnamed Patient"

    def get_absolute_url(self):
        return reverse('nimregenin:patient_update', kwargs={'pk': self.pk})
