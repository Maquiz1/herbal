from django.urls import path

from .views.subjects.lists.subject_list_view import subject_list_view
from .views.subjects.creates.subject_create_view import subject_create_view
from .views.subjects.details.subject_detail_view import subject_detail_view
from .views.subjects.updates.subject_update_view import subject_update_view


app_name = "herbal"

urlpatterns = [

    path("subjects/", subject_list_view, name="subjects-list"),

    path("subjects/create/", subject_create_view, name="subject-create"),
    
    path(
        "subjects/<int:pk>/",
        subject_detail_view,
        name="subjects-detail"
    ),
    
    path(
        "subjects/<int:pk>/edit/",
        subject_update_view,
        name="subjects-update"
    ),

]
