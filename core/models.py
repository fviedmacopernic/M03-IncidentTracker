from django.db import models


class SecurityIncident(models.Model):
    """Model to track security incidents"""
    
    SEVERITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Mitjana'),
        ('HIGH', 'Alta'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='MEDIUM',
        verbose_name='Severidad'
    )
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name='Detectado en')
    
    class Meta:
        verbose_name = 'Incidente de Seguridad'
        verbose_name_plural = 'Incidentes de Seguridad'
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_severity_display()}"
