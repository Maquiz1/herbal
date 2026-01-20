# nimregenin/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    Patient, Screening, Enrollment, Visit,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)


# ==================== CRF Inlines for Visit ====================

class CRF1Inline(admin.TabularInline):
    model = CRF1
    extra = 0
    can_delete = True
    fields = ('height_cm', 'weight_kg', 'bmi', 'medical_history')
    readonly_fields = ('bmi',)


class CRF2Inline(admin.TabularInline):
    model = CRF2
    extra = 0
    fields = ('systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature', 'notes')


class CRF3Inline(admin.TabularInline):
    model = CRF3
    extra = 0
    fields = ('hemoglobin', 'wbc', 'platelets', 'creatinine', 'alt', 'ast')


class CRF4Inline(admin.TabularInline):
    model = CRF4
    extra = 0
    fields = ('no_conmeds', 'medications')


class CRF5Inline(admin.TabularInline):
    model = CRF5
    extra = 0
    fields = ('ae_description', 'severity', 'serious', 'onset_date', 'resolution_date')


class CRF6Inline(admin.TabularInline):
    model = CRF6
    extra = 0
    fields = ('primary_endpoint_score', 'secondary_endpoint_score', 'notes')


class CRF7Inline(admin.TabularInline):
    model = CRF7
    extra = 0
    fields = ('completion_date', 'termination_reason', 'other_reason', 'final_notes')


# ==================== Visit Admin ====================

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = [
        'patient_link',
        'visit_type_display',
        'planned_date',
        'actual_date',
        'completion_status',
        'crf_completion_count',
    ]
    list_filter = ['visit_type', 'completed', 'planned_date', 'actual_date']
    search_fields = ['enrollment__screening__patient__pid']
    date_hierarchy = 'planned_date'
    inlines = [
        CRF1Inline, CRF2Inline, CRF3Inline, CRF4Inline,
        CRF5Inline, CRF6Inline, CRF7Inline
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'enrollment__screening__patient'
        )

    def patient_link(self, obj):
        patient = obj.enrollment.screening.patient
        url = reverse('admin:nimregenin_patient_change', args=[patient.pk])
        return format_html('<a href="{}"><strong>{}</strong></a>', url, patient.pid)
    patient_link.short_description = 'Patient ID'
    patient_link.admin_order_field = 'enrollment__screening__patient__pid'
    def visit_type_display(self, obj):
        return obj.get_visit_type_display()
    visit_type_display.short_description = 'Visit Type'

    def completion_status(self, obj):
        if obj.completed:
            return format_html('<span class="text-success">✓ Completed</span>')
        elif obj.actual_date:
            return format_html('<span class="text-warning">● In Progress</span>')
        else:
            return format_html('<span class="text-muted">○ Pending</span>')
    completion_status.short_description = 'Status'

    def crf_completion_count(self, obj):
        filled = 0
        total = 5  # CRF2, CRF3, CRF4, CRF5, CRF6

        if obj.visit_type == 'BASELINE':
            total += 1  # +CRF1
            if hasattr(obj, 'crf1') and obj.crf1:
                filled += 1

        if obj.visit_type == 'DAY120':
            total += 1  # +CRF7
            if hasattr(obj, 'crf7') and obj.crf7:
                filled += 1

        # Always count these
        if hasattr(obj, 'crf2') and obj.crf2: filled += 1
        if hasattr(obj, 'crf3') and obj.crf3: filled += 1
        if hasattr(obj, 'crf4') and obj.crf4: filled += 1
        if hasattr(obj, 'crf5_aes') and obj.crf5_aes.exists(): filled += 1
        if hasattr(obj, 'crf6') and obj.crf6: filled += 1

        return format_html('<strong>{}/{}</strong>', filled, total)
    crf_completion_count.short_description = 'CRFs Filled'


# ==================== Enrollment Admin with Visit Inline ====================

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    fields = ['visit_type', 'planned_date', 'actual_date', 'completed']
    readonly_fields = ['visit_type', 'planned_date']
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False  # Visits auto-created


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['patient_pid', 'enrollment_date', 'study_id', 'status']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['screening__patient__pid', 'study_id']
    inlines = [VisitInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('screening__patient')
    def patient_pid(self, obj):
        return obj.screening.patient.pid
    patient_pid.short_description = 'Patient ID'
    patient_pid.admin_order_field = 'screening__patient__pid'

# ==================== Patient Admin ====================

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pid', 'full_name', 'age', 'get_gender_display', 'site', 'screening_status', 'enrollment_status']
    list_filter = ['gender', 'site', 'created_at']
    search_fields = ['pid', 'fname', 'lname']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('screening', 'screening__enrollment')

    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Name'

    def screening_status(self, obj):
        if hasattr(obj, 'screening'):
            status = obj.screening.get_screening_status_display()
            color = 'success' if obj.screening.screening_status == 'PASS' else 'danger'
            return format_html('<span class="badge bg-{}">{}</span>', color, status)
        return format_html('<span class="badge bg-secondary">Not Screened</span>')
    screening_status.short_description = 'Screening'

    def enrollment_status(self, obj):
        if hasattr(obj, 'screening') and hasattr(obj.screening, 'enrollment'):
            return format_html('<span class="badge bg-info">Enrolled</span>')
        return format_html('<span class="badge bg-secondary">Not Enrolled</span>')
    enrollment_status.short_description = 'Enrollment'


# ==================== Simple Admins ====================

@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ['patient_pid', 'screening_date', 'screening_status']
    list_filter = ['screening_status', 'screening_date']
    search_fields = ['patient__pid']

    def patient_pid(self, obj):
        return obj.patient.pid
    patient_pid.short_description = 'PID'


# Register CRFs simply (optional - main access via Visit)
admin.site.register([CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7])