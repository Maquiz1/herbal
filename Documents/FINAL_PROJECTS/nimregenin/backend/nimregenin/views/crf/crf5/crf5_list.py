# nimregenin/views/crf5_list.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q

from ....models import CRF5


class CRF5ListView(LoginRequiredMixin, ListView):
    model = CRF5
    template_name = 'nimregenin/crf/crf5/crf5_list.html'
    context_object_name = 'crf5_records'
    paginate_by = 25
    ordering = ['-onset_date', '-created_at']

    def get_queryset(self):
        queryset = CRF5.objects.select_related(
            'visit__enrollment__patient__patient'
        )

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(visit__enrollment__patient__patient__pid__icontains=search) |
                Q(visit__enrollment__patient__patient__fname__icontains=search) |
                Q(visit__enrollment__patient__patient__lname__icontains=search) |
                Q(ae_description__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CRF5 - Adverse Events'
        context['search_term'] = self.request.GET.get('search', '')
        context['total_records'] = CRF5.objects.count()
        return context