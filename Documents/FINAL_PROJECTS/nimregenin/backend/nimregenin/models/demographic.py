from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User
from locations.models import Region, District,Site  # Assuming you have a locations app

class Demographic(models.Model):
    """
    Comprehensive patient demographic and enrollment tracking model
    based on the provided schema.
    """
    # backup_id = models.IntegerField(blank=True, null=True)
    rec_date = models.DateField(blank=True, null=True)
    # Unique identifiers
    pid = models.CharField(max_length=255)
    # Personal identification
    hid = models.CharField(max_length=255, blank=True, null=True)
    nid = models.CharField(max_length=255, blank=True, null=True)
    # Name
    fname = models.CharField(max_length=255, blank=True, null=True)
    mname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    # Demographics
    dob = models.DateField(blank=True, null=True)  # Stored as string per schema
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
    # OCCUPATION_CHOICES = (
    #     ('1', 'Employed'),
    #     ('2', 'Self-Employed'),
    #     ('3', 'Business'),
    #     ('4', 'Other'),
    # )
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_enrolled'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_updated'
    )
    # Status & Comments
    status = models.PositiveIntegerField(default=0)  # Likely a status code
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Patient Demographic"
        verbose_name_plural = "Patient Demographics"
        ordering = ['-created_at']

    def __str__(self):
        name = f"{self.fname or ''} {self.mname or ''} {self.lname or ''}".strip()
        if name:
            return f"{name} ({self.pid or self.study_id or 'No ID'})"
        return self.pid or self.study_id or f"Patient {self.pk}"

    def get_full_name(self):
        return f"{self.fname or ''} {self.mname or ''} {self.lname or ''}".strip() or "Unnamed Patient"

    def get_absolute_url(self):
        return reverse('nimregenin:patient_update', kwargs={'pk': self.pk})
    