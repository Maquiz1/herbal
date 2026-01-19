# nimregenin/views/patient.py

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from ..create_update_view import CreateUpdateView
from ...models import Demographic
from ...forms import DemographicForm


class DemographicCreateUpdateView(CreateUpdateView):
    model = Demographic
    form_class = DemographicForm
    template_name = 'nimregenin/demographic/demographic_form.html'
    success_url = reverse_lazy('nimregenin:patient_list')

    def get_extra_context(self):
        return {
            'title': "Edit Patient" if self.object else "Add New Patient"
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form_class()(
            request.POST,
            instance=self.object,
            request=request   # ✅ pass request into form
        )

        if form.is_valid():
            self.object = form.save()
            self.form_valid_success(form)
            return redirect(self.get_success_url())

        return self.render_form(request, form)

    def form_valid_success(self, form):
        messages.success(
            self.request,
            f"Patient {form.instance.pid} saved successfully."
        )
