from django.contrib import admin
from .models import User
from .models import StaffProfile

admin.site.register(User)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = ("user", "role", "site")

    filter_horizontal = ("assigned_sites",)

