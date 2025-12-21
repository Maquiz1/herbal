"""
create_update.py

Generic base view for handling both Create and Update operations in one class.
Used by all CRF CreateUpdate views for DRY code.
"""

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.http import HttpResponse


class CreateUpdateView(View, LoginRequiredMixin):
    """
    A reusable view that handles both object creation and updating.
    
    Subclasses must define:
        - model: The Django model
        - fields: List of field names or '__all__'
    
    Optional:
        - template_name
        - success_url (or override get_success_url)
    """
    model = None
    fields = None
    template_name = 'nimregenin/crf_form.html'
    success_url = None  # Can be overridden in subclass

    def get_form_class(self):
        """Dynamically create a ModelForm for the model and fields."""
        if not self.model:
            raise ValueError("CreateUpdateView requires a 'model' attribute.")
        if not self.fields:
            raise ValueError("CreateUpdateView requires a 'fields' attribute.")
        
        return modelform_factory(self.model, fields=self.fields)

    def get_object(self, pk=None):
        """Retrieve existing object if pk is provided."""
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return None

    def get(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form_class()(instance=obj)
        return self.render_form(request, form, obj)

    def post(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form_class()(request.POST, instance=obj)
        if form.is_valid():
            self.object = form.save()
            return redirect(self.get_success_url())
        return self.render_form(request, form, obj)

    def render_form(self, request, form, obj):
        """Render the template with form and object context."""
        context = {
            'form': form,
            'object': obj,
            'title': f"{'Edit' if obj else 'Create'} {self.model._meta.verbose_name.title()}",
        }
        # Use render shortcut if available, otherwise fallback
        from django.shortcuts import render
        return render(request, self.template_name, context)

    def get_success_url(self):
        """Return success URL — override in subclass if dynamic."""
        if self.success_url:
            return self.success_url
        raise ValueError(f"No success_url defined for {self.__class__.__name__}")