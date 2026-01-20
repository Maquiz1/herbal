from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..create_update_view import CreateUpdateView
from ..delete import CRFDeleteView
from ...models import Enrollment, Screening, Patient, Visit
from django.core.paginator import Paginator 

class EnrollmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'nimregenin/enrollment/enrollment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '')
        qs = Enrollment.objects.select_related('screening__patient').order_by('-enrollment_date')
        
        if search_term:
            qs = qs.filter(screening__patient__pid__icontains=search_term)
            
        paginator = Paginator(qs, 10)  # 10 per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'enrollments': page_obj,
            'search_term': search_term,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
            'paginator': paginator,
            'title': 'Enrollment Records',
        })
        
        return context