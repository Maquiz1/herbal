from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User


class Demographic(models.Model):
    """
    Comprehensive patient demographic and enrollment tracking model
    based on the provided schema.
    """

    recruitment_date = models.CharField(max_length=12, blank=True, null=True)
    # Unique identifiers
    pid = models.CharField(max_length=50, unique=True)
    # Personal identification
    hospital_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    national_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # Study-related IDs
    # Dates
    previous_date = models.CharField(max_length=12, blank=True, null=True)
    previous_date2 = models.TextField(blank=True, null=True)  # Could be multiple dates
    # Name
    firstname = models.CharField(max_length=16, blank=True, null=True)
    middlename = models.CharField(max_length=16, blank=True, null=True)
    lastname = models.CharField(max_length=16, blank=True, null=True)
    nimregenin = models.CharField(max_length=1, blank=True, null=True)  # Likely a flag (Y/N)

    # Demographics
    dob = models.CharField(max_length=12, blank=True, null=True)  # Stored as string per schema
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, blank=True, null=True)

    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)

    education_level = models.CharField(max_length=25, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    workplace = models.CharField(max_length=50, blank=True, null=True)

    # Contact
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?\d{9,15}$', 'Enter a valid phone number.')]
    )
    other_phone = models.CharField(max_length=16, blank=True, null=True)

    # Address
    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    ward = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    block_no = models.CharField(max_length=15, blank=True, null=True)

    # Enrollment & Screening Flags
    consented = models.BooleanField(default=False)
    consented_nimregenin = models.BooleanField(default=False)
    screened = models.BooleanField(default=False)  # '0'/'1' as boolean
    eligible = models.BooleanField(default=False)
    eligibility1 = models.BooleanField(default=False)
    eligibility2 = models.BooleanField(default=False)
    enrolled = models.BooleanField(default=False)
    end_study = models.BooleanField(default=False)

    # Treatment & Visit Tracking
    pt_type = models.CharField(max_length=1, blank=True, null=True)  # e.g., N=New, R=Return
    patient_category = models.CharField(max_length=2, default='0')
    treatment_type = models.CharField(max_length=1, blank=True, null=True)
    treatment_type2 = models.CharField(max_length=2, blank=True, null=True)

    total_cycle = models.CharField(max_length=255, blank=True, null=True)
    cycle_number = models.CharField(max_length=255, blank=True, null=True)

    # Staff & Site
    SITE_CHOICES = (
        ('1', 'MNH'),
        ('2', 'ORCI'),
    )
    site = models.PositiveIntegerField(choices=SITE_CHOICES)    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients_enrolled'
    )

    # Status & Comments
    status = models.PositiveIntegerField(default=0)  # Likely a status code
    comments = models.TextField(blank=True, null=True)

    # Timestamps
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Patient Demographic"
        verbose_name_plural = "Patient Demographics"
        ordering = ['-created_on']

    def __str__(self):
        name = f"{self.firstname or ''} {self.middlename or ''} {self.lastname or ''}".strip()
        if name:
            return f"{name} ({self.participant_id or self.study_id or 'No ID'})"
        return self.participant_id or self.study_id or f"Patient {self.pk}"

    def get_full_name(self):
        return f"{self.firstname or ''} {self.middlename or ''} {self.lastname or ''}".strip() or "Unnamed Patient"

    def get_absolute_url(self):
        return reverse('nimregenin:patient_update', kwargs={'pk': self.pk})
    
# class Demographic(models.Model):
#     """
#     Patient demographic information.
#     Central model — all other data (screening, enrollment, visits, CRFs) link to this.
#     """

#     # Unique identifier
#     patient_id = models.CharField(
#         max_length=50,
#         unique=True,
#         help_text="Unique patient identifier (e.g., PT-001)"
#     )

#     # Site assignment
#     SITE_CHOICES = (
#         ('SITE001', 'Site 001 - City Hospital'),
#         ('SITE002', 'Site 002 - University Medical Center'),
#         ('SITE003', 'Site 003 - Regional Clinic'),
#         ('SITE004', 'Site 004 - Private Practice'),
#         # Add more sites as needed
#     )
#     site = models.CharField(
#         max_length=20,  # Matches longest code
#         choices=SITE_CHOICES,
#         blank=True,
#         null=True,
#         help_text="Clinical site where patient is enrolled"
#     )

#     # Demographics
#     date_of_birth = models.DateField(
#         null=True,
#         blank=True,
#         help_text="Patient's date of birth"
#     )
#     age = models.PositiveIntegerField(
#         null=True,
#         blank=True,
#         validators=[MinValueValidator(0), MaxValueValidator(120)],
#         help_text="Patient age in years (0–120)"
#     )

#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#         ('U', 'Unknown'),
#     )
#     gender = models.CharField(
#         max_length=1,
#         choices=GENDER_CHOICES,
#         blank=True,
#         help_text="Patient gender"
#     )

#     ethnicity = models.CharField(
#         max_length=100,
#         blank=True,
#         help_text="Ethnicity (e.g., Hispanic or Latino)"
#     )
#     race = models.CharField(
#         max_length=100,
#         blank=True,
#         help_text="Race (e.g., White, Asian, Black)"
#     )

#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Demographics"
#         ordering = ['-created_at']

#     def __str__(self):
#         """Human-readable representation"""
#         site_name = f" ({self.get_site_display()})" if self.site else ""
#         return f"{self.patient_id}{site_name}"

#     def get_absolute_url(self):
#         """URL to edit this patient"""
#         return reverse('nimregenin:patient_update', kwargs={'pk': self.pk})


class Screening(models.Model):
    patient = models.OneToOneField(Demographic, on_delete=models.CASCADE, related_name='screening')
    screening_date = models.DateField()
    
    STATUS_CHOICES = (
        ('PASS', 'Passed'),
        ('FAIL', 'Failed'),
        ('PENDING', 'Pending'),
    )
    screening_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True)
    screened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Screening - {self.patient.patient_id}"

    @property
    def patient_id(self):
        return self.patient.patient_id


class Enrollment(models.Model):
    patient = models.OneToOneField(Demographic, on_delete=models.CASCADE, related_name='enrollment')
    enrollment_date = models.DateField()
    study_id = models.CharField(max_length=50, blank=True)
    randomization_number = models.CharField(max_length=50, blank=True)
    
    STATUS_CHOICES = (
        ('ENROLLED', 'Enrolled'),
        ('RANDOMIZED', 'Randomized'),
        ('WITHDRAWN', 'Withdrawn'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ENROLLED')
    enrolled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.patient_id} - Enrolled {self.enrollment_date}"


class Visit(models.Model):
    VISIT_TYPES = (
        ('BASELINE', 'Baseline (Day 0)'),
        ('DAY7', 'Day 7'),
        ('DAY14', 'Day 14'),
        ('DAY30', 'Day 30'),
        ('DAY60', 'Day 60'),
        ('DAY90', 'Day 90'),
        ('DAY120', 'Day 120'),
    )
    
    patient = models.ForeignKey(Demographic, on_delete=models.CASCADE, related_name='visits')
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES)
    planned_date = models.DateField(null=True, blank=True)
    actual_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('patient', 'visit_type')

    def __str__(self):
        return f"{self.get_visit_type_display()} - {self.patient.patient_id}"


# # CRF Models (Case Report Forms 1 through 7)
class CRF1(models.Model):
    """CRF1 - Baseline Visit / Medical History"""
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='crf1', limit_choices_to={'visit_type': 'BASELINE'})
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    medical_history = models.TextField(blank=True)
    concomitant_medications = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF1 - {self.patient_id} ({self.visit_date})"


class CRF2(models.Model):
    """CRF2 - Physical Examination"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='crf2')
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    physical_exam_findings = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF2 - {self.patient_id} ({self.visit_date})"


class CRF3(models.Model):
    """CRF3 - Laboratory Results"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='crf3')
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    hemoglobin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wbc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    platelets = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    creatinine = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    alt = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    ast = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF3 - {self.patient_id} ({self.visit_date})"


class CRF4(models.Model):
    """CRF4 - Adverse Events"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='crf4')
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    ae_description = models.TextField()
    severity = models.CharField(max_length=20, choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')])
    serious = models.BooleanField(default=False)
    outcome = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF4 AE - {self.patient_id} ({self.ae_start_date})"


class CRF5(models.Model):
    """CRF5 - Concomitant Medications Update"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='crf5')
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    medication_name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF5 Med - {self.patient_id} ({self.medication_name})"


class CRF6(models.Model):
    """CRF6 - Efficacy Assessment"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='crf6')
#     patient_id = models.CharField(max_length=50)
    visit_date = models.DateField(null=True, blank=True)
    primary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    secondary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    clinician_assessment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF6 - {self.patient_id} ({self.visit_date})"


class CRF7(models.Model):
    """CRF7 - Study Completion / Early Termination"""
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='crf7', limit_choices_to={'visit_type__in': ['DAY90', 'DAY120']})
    # patient_id = models.CharField(max_length=50)
    completion_date = models.DateField(null=True, blank=True)
    early_termination = models.BooleanField(default=False)
    termination_reason = models.TextField(blank=True)
    study_completion_status = models.CharField(max_length=20, choices=[('COMPLETED', 'Completed'), ('TERMINATED', 'Terminated')], blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF7 - {self.patient_id} ({self.study_completion_status or 'Pending'})"
