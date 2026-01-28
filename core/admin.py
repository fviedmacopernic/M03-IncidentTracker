from django.contrib import admin
from .models import SecurityIncident


@admin.register(SecurityIncident)
class SecurityIncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'detected_at')
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
