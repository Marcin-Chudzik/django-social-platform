from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'formatted_date_of_birth', 'photo']
    list_of_fields = ['user', 'date_of_birth', 'photo']

    def formatted_date_of_birth(self, obj) -> object:
        return obj.date_of_birth.strftime('%Y-%m-%d')
    formatted_date_of_birth.short_description = 'Date of Birth'
