from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Demographic(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(120)])
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    )
    
    SITE_CHOICES = (
        ('SITE001', 'Site 001 - City Hospital'),
        ('SITE002', 'Site 002 - University Medical Center'),
        ('SITE003', 'Site 003 - Regional Clinic'),
        ('SITE004', 'Site 004 - Private Practice'),
        # Add your real sites
    )
    site = models.CharField(max_length=200, choices=SITE_CHOICES, blank=True, null=True)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    ethnicity = models.CharField(max_length=100, blank=True)
    race = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient_id

    class Meta:
        verbose_name_plural = "Demographics"


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
