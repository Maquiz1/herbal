# nimregenin/views/patient.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ...models import Patient


class PatientListView(LoginRequiredMixin, ListView):
    """
    Simple patient registry list.
    Shows all patients from Demographic with screening and enrollment status.
    No visit logic included.
    """
    model = Patient
    template_name = 'nimregenin/patient/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 25
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Base queryset: all Patients with related site, screening, and enrollment.
        """
        queryset = Patient.objects.select_related(
            'site',
            'screening',           # OneToOne to Screening
            'screening__enrollment'  # OneToOne from Screening to Enrollment
        )

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(pid__icontains=search) |
                Q(fname__icontains=search) |
                Q(lname__icontains=search) |
                Q(phone_patient__icontains=search) |
                Q(nid__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Patient Registry'

        # Summary statistics using correct OneToOne chain
        context['total_patients'] = Patient.objects.count()
        context['total_screened'] = Patient.objects.filter(screening__isnull=False).count()
        context['total_enrolled'] = Patient.objects.filter(
            screening__enrollment__isnull=False
        ).count()

        context['search_term'] = self.request.GET.get('search', '')

        return context