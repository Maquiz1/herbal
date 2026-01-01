# nimregenin/views/crf1_list.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ....models import CRF1


class CRF1ListView(LoginRequiredMixin, ListView):
    model = CRF1
    template_name = 'nimregenin/crf/crf1/crf1_list.html'
    context_object_name = 'crf1_records'
    paginate_by = 25
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = CRF1.objects.select_related(
            'visit__enrollment__patient__patient'
        ).only(
            'visit__enrollment__patient__patient__pid',
            'visit__enrollment__patient__patient__fname',
            'visit__enrollment__patient__patient__lname',
            'height_cm',
            'weight_kg',
            'bmi',
            'created_at'
        )

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(visit__enrollment__patient__patient__pid__icontains=search) |
                Q(visit__enrollment__patient__patient__fname__icontains=search) |
                Q(visit__enrollment__patient__patient__lname__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CRF1 - Baseline Assessments'
        context['search_term'] = self.request.GET.get('search', '')
        context['total_records'] = CRF1.objects.count()
        return context