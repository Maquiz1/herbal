from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.forms import modelform_factory
from django.contrib import messages


class CreateUpdateView(LoginRequiredMixin, View):
    model = None
    fields = None
    form_class = None
    template_name = 'nimregenin/crf_form.html'
    success_url = None

    def get_form_class(self):
        if self.form_class:
            return self.form_class
        if not self.model or not self.fields:
            raise ValueError("model and fields must be defined")
        return modelform_factory(self.model, fields=self.fields)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(
            instance=self.object,
            request=request
        )
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            request=request
        )

        if form.is_valid():
            self.object = form.save(commit=False)
            # ✅ AuditModel handles created_by/updated_by internally
            self.object.save(user=request.user)

            self.form_valid_success(form)
            return redirect(self.get_success_url())

        return self.render_form(request, form)


    def render_form(self, request, form):
        context = {
            'form': form,
            'object': self.object,
            'title': self.get_page_title(),
        }
        context.update(self.get_extra_context())
        return render(request, self.template_name, context)

    def get_page_title(self):
        action = "Edit" if self.object else "Create"
        return f"{action} {self.model._meta.verbose_name.title()}"

    def get_extra_context(self):
        return {}

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        if self.object and hasattr(self.object, 'get_absolute_url'):
            return self.object.get_absolute_url()
        raise ValueError("No success_url defined")

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"{self.model._meta.verbose_name.title()} saved successfully."
        )
