"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import (
    perfil_usuari,
    cerca_form,
    cerca_resultats_vulnerable,
    cerca_resultats_segura,
    actualitzar_email_vulnerable,
    actualitzar_email_segur,
    incident_detall_vulnerable,
    incident_detall_segur,
    incident_llista,
    api_get_incidents,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Autenticació
    path('accounts/', include('django.contrib.auth.urls')),
    path('perfil/', perfil_usuari, name='perfil'),
    
    # APARTAT 2 & 3: Cerca d'incidents (VULNERABLE)
    path('cerca/', cerca_form, name='cerca'),
    path('cerca/resultats/', cerca_resultats_vulnerable, name='cerca_resultats'),
    
    # APARTAT 4: Actualització d'email (VULNERABLE - Privilege Escalation)
    path('actualitzar-email/', actualitzar_email_vulnerable, name='actualitzar_email'),
    
    # APARTAT 7: Detall d'incident (VULNERABLE - IDOR)
    path('incident/<int:id>/', incident_detall_vulnerable, name='incident_detall_vulnerable'),
    
    # APARTAT 9: Llista d'incidents (XSS amb |safe)
    path('incidents/', incident_llista, name='incident_llista'),
    
    # VERSIONS SEGURES (APARTAT 6 & 8)
    path('secure/cerca/resultats/', cerca_resultats_segura, name='cerca_resultats_segura'),
    path('secure/actualitzar-email/', actualitzar_email_segur, name='actualitzar_email_segur'),
    path('secure/incident/<int:id>/', incident_detall_segur, name='incident_detall_segur'),

    # PART 6 — P6: API JSON per a l'App Mòbil
    path('api/incidents/', api_get_incidents, name='api_get_incidents'),
]
