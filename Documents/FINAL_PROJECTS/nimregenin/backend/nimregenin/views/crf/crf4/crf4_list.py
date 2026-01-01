# nimregenin/views/crf4_list.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ....models import CRF4


class CRF4ListView(LoginRequiredMixin, ListView):
    model = CRF4
    template_name = 'nimregenin/crf/crf4/crf4_list.html'
    context_object_name = 'crf4_records'
    paginate_by = 25
    ordering = ['-visit_date', '-created_at']

    def get_queryset(self):
        queryset = CRF4.objects.select_related(
            'visit__enrollment__patient__patient'
        )

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(visit__enrollment__patient__patient__pid__icontains=search) |
                Q(visit__enrollment__patient__patient__fname__icontains=search) |
                Q(visit__enrollment__patient__patient__lname__icontains=search) |
                Q(medications__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CRF4 - Concomitant Medications'
        context['search_term'] = self.request.GET.get('search', '')
        context['total_records'] = CRF4.objects.count()
        return context