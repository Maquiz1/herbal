from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Demographic(models.Model):
    """Patient demographic information"""
    # patient_id = models.CharField(max_length=50, unique=True, help_text="Unique patient identifier")
    # date_of_birth = models.DateField(null=True, blank=True)
    # age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(120)])
    
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('O', 'Other'),
    #     ('U', 'Unknown/Prefer not to say'),
    # )
    # gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # ethnicity = models.CharField(max_length=100, blank=True)
    # race = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Demographic - {self.patient_id}"


class Screening(models.Model):
    """Screening visit data"""
#     patient_id = models.CharField(max_length=50, unique=True)
#     screening_date = models.DateField()
    
#     SCREENING_STATUS_CHOICES = (
#         ('PASS', 'Passed'),
#         ('FAIL', 'Failed'),
#         ('PENDING', 'Pending Review'),
#     )
#     screening_status = models.CharField(max_length=10, choices=SCREENING_STATUS_CHOICES)
#     failure_reason = models.TextField(blank=True)
    
#     screened_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='screenings')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Screening - {self.patient_id} ({self.screening_status})"


class Enrollment(models.Model):
    """Enrollment and randomization data"""
#     patient_id = models.CharField(max_length=50, unique=True)
#     enrollment_date = models.DateField()
#     study_id = models.CharField(max_length=50, blank=True)
#     randomization_number = models.CharField(max_length=50, blank=True, help_text="If randomized")
    
#     ENROLLMENT_STATUS_CHOICES = (
#         ('ENROLLED', 'Enrolled'),
#         ('RANDOMIZED', 'Randomized'),
#         ('WITHDRAWN', 'Withdrawn'),
#     )
#     status = models.CharField(max_length=15, choices=ENROLLMENT_STATUS_CHOICES, default='ENROLLED')
    
#     enrolled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='enrollments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Enrollment - {self.patient_id} ({self.status})"


# # CRF Models (Case Report Forms 1 through 7)
class CRF1(models.Model):
    """CRF1 - Baseline Visit / Medical History"""
#     patient_id = models.CharField(max_length=50)
#     visit_date = models.DateField()
#     height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
#     medical_history = models.TextField(blank=True)
#     concomitant_medications = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF1 - {self.patient_id} ({self.visit_date})"


class CRF2(models.Model):
    """CRF2 - Physical Examination"""
#     patient_id = models.CharField(max_length=50)
#     visit_date = models.DateField()
#     systolic_bp = models.PositiveIntegerField(null=True, blank=True)
#     diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
#     heart_rate = models.PositiveIntegerField(null=True, blank=True)
#     physical_exam_findings = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF2 - {self.patient_id} ({self.visit_date})"


class CRF3(models.Model):
    """CRF3 - Laboratory Results"""
#     patient_id = models.CharField(max_length=50)
#     visit_date = models.DateField()
#     hemoglobin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     wbc = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#     platelets = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
#     creatinine = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
#     alt = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
#     ast = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF3 - {self.patient_id} ({self.visit_date})"


class CRF4(models.Model):
    """CRF4 - Adverse Events"""
#     patient_id = models.CharField(max_length=50)
#     ae_start_date = models.DateField()
#     ae_description = models.TextField()
#     severity = models.CharField(max_length=20, choices=[('MILD', 'Mild'), ('MODERATE', 'Moderate'), ('SEVERE', 'Severe')])
#     serious = models.BooleanField(default=False)
#     outcome = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF4 AE - {self.patient_id} ({self.ae_start_date})"


class CRF5(models.Model):
    """CRF5 - Concomitant Medications Update"""
#     patient_id = models.CharField(max_length=50)
#     visit_date = models.DateField()
#     medication_name = models.CharField(max_length=200)
#     dose = models.CharField(max_length=100, blank=True)
#     start_date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF5 Med - {self.patient_id} ({self.medication_name})"


class CRF6(models.Model):
    """CRF6 - Efficacy Assessment"""
#     patient_id = models.CharField(max_length=50)
#     visit_date = models.DateField()
#     primary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#     secondary_endpoint_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#     clinician_assessment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF6 - {self.patient_id} ({self.visit_date})"


class CRF7(models.Model):
    """CRF7 - Study Completion / Early Termination"""
#     patient_id = models.CharField(max_length=50)
#     completion_date = models.DateField(null=True, blank=True)
#     early_termination = models.BooleanField(default=False)
#     termination_reason = models.TextField(blank=True)
#     study_completion_status = models.CharField(max_length=20, choices=[('COMPLETED', 'Completed'), ('TERMINATED', 'Terminated')], blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"CRF7 - {self.patient_id} ({self.study_completion_status or 'Pending'})"