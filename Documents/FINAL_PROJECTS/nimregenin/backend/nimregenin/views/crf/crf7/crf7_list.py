# nimregenin/views/crf7_list.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ....models import CRF7


class CRF7ListView(LoginRequiredMixin, ListView):
    model = CRF7
    template_name = 'nimregenin/crf/crf7/crf7_list.html'
    context_object_name = 'crf7_records'
    paginate_by = 25
    ordering = ['-visit_date', '-created_at']

    def get_queryset(self):
        queryset = CRF7.objects.select_related(
            'visit__enrollment__patient__patient'
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
        context['title'] = 'CRF7 - Efficacy Assessments'
        context['search_term'] = self.request.GET.get('search', '')
        context['total_records'] = CRF7.objects.count()
        return context