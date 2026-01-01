# nimregenin/views/crf6_list.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ....models import CRF6


class CRF6ListView(LoginRequiredMixin, ListView):
    model = CRF6
    template_name = 'nimregenin/crf/crf6/crf6_list.html'
    context_object_name = 'crf6_records'
    paginate_by = 25
    ordering = ['-completion_date', '-created_at']

    def get_queryset(self):
        queryset = CRF6.objects.select_related(
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
        context['title'] = 'CRF6 - Study Completion / Termination'
        context['search_term'] = self.request.GET.get('search', '')
        context['total_records'] = CRF6.objects.count()
        return context