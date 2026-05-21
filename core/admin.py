from django.contrib import admin
from .models import SecurityIncident


@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'detected_at', 'creator')
    list_filter = ('severity', 'detected_at')
    search_fields = ('title', 'description')
    readonly_fields = ('detected_at',)

    fieldsets = (
        ('Información del Incidente', {
            'fields': ('title', 'description', 'severity')
        }),
        ('Metadata', {
            'fields': ('detected_at',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Auto-assigna el creator a l'usuari admin que ha fet login.
        Resol l'error: creator_id NO NULL constraint failed.
        """
        if not change:  # Només en crear (no en editar)
            obj.creator = request.user
        super().save_model(request, obj, form, change)
