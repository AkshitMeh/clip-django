from django.contrib import admin
from .models import Paste

@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ('code', 'content_type', 'created_at', 'expires_at')
    search_fields = ('code', 'text_content')
    list_filter = ('content_type', 'expires_at')
    ordering = ('-created_at',)
    actions = ['delete_selected']  # Enable bulk delete

    def has_delete_permission(self, request, obj=None):
        return True  # Allow delete for all users with change/delete perms
