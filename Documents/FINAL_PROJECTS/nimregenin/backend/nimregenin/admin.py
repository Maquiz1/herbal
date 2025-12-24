from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    Demographic, Screening, Enrollment, Visit,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)

# Inline CRFs for Visit Admin
class CRF1Inline(admin.TabularInline):
    model = CRF1
    extra = 0
    can_delete = True

class CRF2Inline(admin.TabularInline):
    model = CRF2
    extra = 0

class CRF3Inline(admin.TabularInline):
    model = CRF3
    extra = 0

class CRF4Inline(admin.TabularInline):
    model = CRF4
    extra = 0

class CRF5Inline(admin.TabularInline):
    model = CRF5
    extra = 0

class CRF6Inline(admin.TabularInline):
    model = CRF6
    extra = 0

class CRF7Inline(admin.TabularInline):
    model = CRF7
    extra = 0


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = [
        'patient_link',
        'get_visit_type_display',
        'planned_date',
        'actual_date',
        'completion_status',
        'crf_completion_count',
    ]
    list_filter = ['visit_type', 'completed', 'actual_date', 'planned_date']
    search_fields = ['patient__patient_id']
    date_hierarchy = 'planned_date'
    inlines = [CRF1Inline, CRF2Inline, CRF3Inline, CRF4Inline, CRF5Inline, CRF6Inline, CRF7Inline]

    def patient_link(self, obj):
        url = reverse('admin:nimregenin_demographic_change', args=[obj.patient.pk])
        return format_html('<a href="{}"><strong>{}</strong></a>', url, obj.patient.patient_id)
    patient_link.short_description = 'Patient ID'

    def completion_status(self, obj):
        if obj.completed:
            return format_html('<span class="text-success">✓ Completed</span>')
        elif obj.actual_date:
            return format_html('<span class="text-warning">● In Progress</span>')
        else:
            return format_html('<span class="text-muted">○ Pending</span>')
    completion_status.short_description = 'Status'

    def crf_completion_count(self, obj):
        required = 5  # CRF2-6
        if obj.visit_type == 'BASELINE':
            required += 1  # +CRF1
        if obj.visit_type == 'DAY120':
            required += 1  # +CRF7

        filled = sum([
            bool(obj.crf1.exists()) if obj.visit_type == 'BASELINE' else 0,
            obj.crf2.exists(),
            obj.crf3.exists(),
            obj.crf4.exists(),
            obj.crf5.exists(),
            obj.crf6.exists(),
            bool(obj.crf7.exists()) if obj.visit_type == 'DAY120' else 0,
        ])

        return format_html('<strong>{}/{}</strong>', filled, required)
    crf_completion_count.short_description = 'CRFs Filled'


# Improve Demographic Admin to show visits
class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    fields = ['visit_type', 'planned_date', 'actual_date', 'completed']
    readonly_fields = ['visit_type', 'planned_date']
    can_delete = False

    def has_add_permission(self, request, obj):
        return False  # Visits are auto-created


@admin.register(Demographic)
class DemographicAdmin(admin.ModelAdmin):
    list_display = ['pid', 'age', 'get_gender_display', 'created_at', 'visit_progress']
    list_filter = ['gender', 'created_at']
    search_fields = ['pid']
    inlines = [VisitInline]

    def enrollment_status(self, obj):
        if hasattr(obj, 'enrollment'):
            return format_html('<span class="text-success">Enrolled</span>')
        return format_html('<span class="text-muted">Not enrolled</span>')
    enrollment_status.short_description = 'Enrollment'

    def visit_progress(self, obj):
        visits = obj.visits.all()
        if not visits:
            return "No visits"
        completed = visits.filter(completed=True).count()
        total = visits.count()
        return f"{completed}/{total} visits complete"
    visit_progress.short_description = 'Visit Progress'


# Register other models simply
@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'screening_date', 'screening_status']
    list_filter = ['screening_status', 'screening_date']
    search_fields = ['patient_id']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'enrollment_date', 'study_id', 'status']
    list_filter = ['status', 'enrollment_date']
    search_fields = ['patient__patient_id', 'study_id']


# Register CRFs (optional - since they're in Visit inlines, you may not need separate pages)
admin.site.register(CRF1)
admin.site.register(CRF2)
admin.site.register(CRF3)
admin.site.register(CRF4)
admin.site.register(CRF5)
admin.site.register(CRF6)
admin.site.register(CRF7)