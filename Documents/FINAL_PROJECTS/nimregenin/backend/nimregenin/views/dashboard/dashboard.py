# nimregenin/views/home.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q

from ...models import Patient, Screening, Enrollment, CRF6


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard home page after login.
    Shows key recruitment and study status statistics.
    """
    template_name = 'nimregenin/dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nimregenin Registry Dashboard'

        # Total registered patients
        context['total_patients'] = Patient.objects.count()

        # Screened patients (have a screening record)
        context['screened_patients'] = Patient.objects.filter(screening__isnull=False).count()

        # Eligible patients (screened and passed)
        context['eligible_patients'] = Patient.objects.filter(
            screening__screening_status='PASS'
        ).count()

        # Enrolled patients
        context['enrolled_patients'] = Patient.objects.filter(
            screening__enrollment__isnull=False
        ).count()

        # Completed study (CRF6 with status COMPLETED)
        context['completed_patients'] = CRF6.objects.filter(
            study_completion_status='COMPLETED'
        ).count()

        # Terminated / Withdrawn / LTFU / Death (early termination)
        context['terminated_patients'] = CRF6.objects.filter(
            early_termination=True
        ).count()

        # Breakdown of termination reasons (optional for dashboard cards)
        termination_breakdown = CRF6.objects.filter(
            early_termination=True
        ).values('termination_reason').annotate(count=Count('id'))

        context['termination_breakdown'] = {
            'DEATH': 0,
            'WITHDRAWN': 0,
            'LTFU': 0,
            'OTHER': 0,
        }
        for item in termination_breakdown:
            reason = item['termination_reason']
            if reason in context['termination_breakdown']:
                context['termination_breakdown'][reason] = item['count']

        return context