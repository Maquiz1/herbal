"""
create_update.py

Generic base view for handling both Create and Update operations in one class.
Used by all CRF and patient forms for DRY code.
"""

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.contrib import messages


class CreateUpdateView(View, LoginRequiredMixin):
    """
    A reusable view that handles both object creation and updating.

    Subclasses must define:
        - model: The Django model class
        - fields: List of field names (or '__all__')

    Optional:
        - form_class: Custom ModelForm (overrides dynamic form)
        - template_name
        - success_url (or override get_success_url)
    """
    model = None
    fields = None
    form_class = None  # Allows using a custom form instead of dynamic
    template_name = 'nimregenin/crf_form.html'
    success_url = None

    def get_form_class(self):
        """Return form class — custom if provided, otherwise dynamic."""
        if self.form_class:
            return self.form_class

        if not self.model:
            raise ValueError("CreateUpdateView requires a 'model' attribute.")
        if not self.fields:
            raise ValueError("CreateUpdateView requires a 'fields' attribute when no form_class is provided.")

        return modelform_factory(self.model, fields=self.fields)

    def get_object(self, pk=None):
        """Retrieve existing object if pk is provided."""
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return None

    def dispatch(self, request, pk=None, *args, **kwargs):
        """Store pk from URL for use in get/post."""
        self.kwargs['pk'] = pk
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form_class()(instance=obj)
        return self.render_form(request, form, obj)

    def post(self, request, pk=None, *args, **kwargs):
        obj = self.get_object(pk)
        form = self.get_form_class()(request.POST, instance=obj)
        if form.is_valid():
            self.object = form.save()
            self.form_valid_success(form)  # Hook for messages, etc.
            return redirect(self.get_success_url())
        return self.render_form(request, form, obj)

    def render_form(self, request, form, obj):
        """Render the form template."""
        context = {
            'form': form,
            'object': obj,
            'title': self.get_page_title(obj),
        }
        return render(request, self.template_name, context)

    def get_page_title(self, obj):
        """Dynamic page title."""
        action = "Edit" if obj else "Create"
        model_name = self.model._meta.verbose_name.title()
        return f"{action} {model_name}"

    def get_success_url(self):
        """Return success URL — override in subclass if needed."""
        if self.success_url:
            return self.success_url
        if self.object:
            # Try get_absolute_url if model has it
            if hasattr(self.object, 'get_absolute_url'):
                return self.object.get_absolute_url()
        raise ValueError(f"No success_url defined for {self.__class__.__name__}")

    def form_valid_success(self, form):
        """
        Hook for success actions (e.g., messages).
        Override or extend in subclasses.
        """
        messages.success(
            self.request,
            f"{self.model._meta.verbose_name.title()} saved successfully."
        )