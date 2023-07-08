from django.contrib import admin
from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'formatted_created']
    list_of_fields = ['user', 'verb', 'target', 'created']
    list_filter = ['created', ]
    search_fields = ['verb', ]

    def formatted_created(self, obj) -> object:
        return obj.created.strftime(
            "%Y-%m-%d %H:%M:%S.%f%z")[:-2] + ":" +\
               obj.created.strftime("%z")[-2:]
    formatted_created.short_description = 'Created'
