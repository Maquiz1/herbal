from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class TemplateDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/template_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit_type = self.kwargs.get('visit_type', 'BASELINE')

        templates = {
            'BASELINE': {
                'title': 'Baseline Visit (Day 0)',
                'window': 'Day 0',
                'required': ['CRF1', 'CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6'],
                'notes': 'Height, weight, medical history, randomization.'
            },
            'DAY7': {'title': 'Day 7 Follow-up', 'window': 'Day 7 ± 3', 'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6']},
            'DAY14': {'title': 'Day 14 Follow-up', 'window': 'Day 14 ± 3', 'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6']},
            'DAY30': {'title': 'Day 30 Follow-up', 'window': 'Day 30 ± 7', 'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6']},
            'DAY60': {'title': 'Day 60 Follow-up', 'window': 'Day 60 ± 7', 'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6']},
            'DAY90': {'title': 'Day 90 Follow-up', 'window': 'Day 90 ± 7', 'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6']},
            'DAY120': {
                'title': 'Final Visit (Day 120)',
                'window': 'Day 120 ± 10',
                'required': ['CRF2', 'CRF3', 'CRF4', 'CRF5', 'CRF6', 'CRF7'],
                'notes': 'Final efficacy and safety assessment.'
            },
        }

        context['template'] = templates.get(visit_type, templates['BASELINE'])
        return context