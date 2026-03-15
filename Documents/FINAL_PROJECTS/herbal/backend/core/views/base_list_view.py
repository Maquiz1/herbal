from django.views.generic import ListView


class BaseListView(ListView):

    paginate_by = 10
    search_fields = []
    filter_fields = []

    def get_queryset(self):

        qs = super().get_queryset()

        request = self.request

        # SEARCH
        search = request.GET.get("search")

        if search and self.search_fields:

            query = None

            from django.db.models import Q

            for field in self.search_fields:

                q = Q(**{f"{field}__icontains": search})

                query = q if query is None else query | q

            qs = qs.filter(query)

        # FILTERS
        for field in self.filter_fields:

            value = request.GET.get(field)

            if value:
                qs = qs.filter(**{field: value})

        return qs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get("search", "")

        return context
