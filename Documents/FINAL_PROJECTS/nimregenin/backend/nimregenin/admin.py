from django.contrib import admin
from .models import (
    Demographic, Screening, Enrollment,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)

@admin.register(Demographic)
class DemographicAdmin(admin.ModelAdmin):
    # list_display = ('patient_id', 'date_of_birth', 'gender')
    # search_fields = ('patient_id',)
    sortable_by = ('created_at',)

# Register the rest simply
admin.site.register(Screening)
admin.site.register(Enrollment)
admin.site.register(CRF1)
admin.site.register(CRF2)
admin.site.register(CRF3)
admin.site.register(CRF4)
admin.site.register(CRF5)
admin.site.register(CRF6)
admin.site.register(CRF7)