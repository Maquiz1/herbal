from django.urls import path
from .views.dashboard import dashboard_view


app_name = "dashboard"

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
]
