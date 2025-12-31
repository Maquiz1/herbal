# nimregenin/views/home.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from ...models import Demographic, Screening, Enrollment


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard home page after login.
    Shows key recruitment statistics.
    """
    template_name = 'nimregenin/dashboard/home.html'  # Adjust path if needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NIM Regenin Registry Dashboard'

        # Total registered patients
        context['total_patients'] = Demographic.objects.count()

        # Screened patients (any screening record exists)
        context['screened_patients'] = Demographic.objects.filter(screening__isnull=False).count()

        # Eligible patients (screened and passed)
        context['eligible_patients'] = Demographic.objects.filter(
            screening__screening_status='PASS'
        ).count()

        # Enrolled patients (have enrollment via screening)
        context['enrolled_patients'] = Demographic.objects.filter(
            screening__enrollment__isnull=False
        ).count()

        # Study Termination / Withdrawn (example: status == 'WITHDRAWN')
        context['terminated_patients'] = Demographic.objects.filter(
            screening__enrollment__status='WITHDRAWN'
        ).count()

        # Loss to Follow-Up (you can customize this logic later)
        # Example: enrolled but no recent activity — placeholder
        context['ltf_patients'] = 0  # Replace with real logic when ready

        return context