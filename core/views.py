from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SecurityIncident

# ============================================
# APARTAT 2 & 3: CERCA VULNERABLE (SQL INJECTION)
# ============================================

@login_required
def cerca_form(request):
    """Formulari de cerca d'incidents"""
    return render(request, 'cerca.html')

@login_required
def cerca_resultats_vulnerable(request):
    """
    VULNERABILITAT: SQL Injection
    Aquesta vista utilitza SQL RAW amb concatenació directa.
    NO utilitza l'ORM de Django.
    LÍNIA VULNERABLE: La concatenació directa de 'query' a la SQL string.
    """
    query = request.GET.get('q', '')
    
    # VULNERABILITAT: Concatenació directa sense sanitització
    sql = f"SELECT title, description, creator_id, detected_at FROM core_securityincident WHERE title LIKE '%{query}%'"
    
    with connection.cursor() as cursor:
        cursor.execute(sql)  # LÍNIA VULNERABLE
        incidents = cursor.fetchall()
    
    return render(request, 'cerca_resultats.html', {
        'incidents': incidents,
        'query': query
    })

# ============================================
# APARTAT 4: ACTUALITZACIÓ D'EMAIL VULNERABLE (PRIVILEGE ESCALATION)
# ============================================

@login_required
def actualitzar_email_vulnerable(request):
    """
    VULNERABILITAT: SQL Injection + Privilege Escalation
    Permet modificar is_superuser mitjançant payload al camp email.
    """
    message = ""
    
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        # ⚠️ VULNERABILITAT: SQL concatenat sense prepared statements
        sql = f"UPDATE auth_user SET email = '{email}' WHERE id = {request.user.id}"
        
        with connection.cursor() as cursor:
            cursor.execute(sql)  # ⚠️ LÍNIA VULNERABLE
        
        message = "Email actualitzat correctament!"
    
    return render(request, 'actualitzar_email.html', {
        'message': message,
        'current_email': request.user.email
    })

# ============================================
# APARTAT 7: DETALL D'INCIDENT VULNERABLE (IDOR)
# ============================================

@login_required
def incident_detall_vulnerable(request, id):
    """
    VULNERABILITAT: Insecure Direct Object Reference (IDOR)
    No verifica que l'usuari sigui el propietari de l'incident.
    """
    # ⚠️ VULNERABILITAT: No verifica creator = request.user
    incident = get_object_or_404(SecurityIncident, id=id)
    
    return render(request, 'incident_detall.html', {
        'incident': incident
    })

# ============================================
# APARTAT 9: LLISTA D'INCIDENTS (XSS)
# ============================================

@login_required
def incident_llista(request):
    """
    Llista d'incidents de l'usuari actual.
    La vulnerabilitat XSS està a la plantilla amb |safe
    """
    incidents = SecurityIncident.objects.filter(creator=request.user)
    
    return render(request, 'incident_llista.html', {
        'incidents': incidents
    })

# ============================================
# VERSIONS SEGURES (HARDENED) - APARTAT 6 & 8
# ============================================

@login_required
def cerca_resultats_segura(request):
    """
    VERSIÓ SEGURA: Utilitza ORM amb prepared statements
    """
    query = request.GET.get('q', '')
    
    # ✅ SEGUR: L'ORM parametritza automàticament
    incidents = SecurityIncident.objects.filter(
        title__icontains=query,
        creator=request.user  # També aplica control d'accés
    )
    
    return render(request, 'cerca_resultats_segura.html', {
        'incidents': incidents,
        'query': query
    })

@login_required
def actualitzar_email_segur(request):
    """
    VERSIÓ SEGURA: Utilitza ORM amb update()
    """
    message = ""
    
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        # ✅ SEGUR: L'ORM parametritza automàticament
        request.user.email = email
        request.user.save()
        
        message = "Email actualitzat correctament!"
    
    return render(request, 'actualitzar_email.html', {
        'message': message,
        'current_email': request.user.email
    })

@login_required
def incident_detall_segur(request, id):
    """
    VERSIÓ SEGURA: Verifica que l'usuari sigui el propietari
    """
    # ✅ SEGUR: Filtra per creator = request.user
    incident = get_object_or_404(SecurityIncident, id=id, creator=request.user)
    
    return render(request, 'incident_detall.html', {
        'incident': incident
    })

# ============================================
# PART 6 — P6: API JSON PER A L'APP MÒBIL
# ============================================

@csrf_exempt
def api_get_incidents(request):
    """
    API pública JSON per a l'App mòbil Android.
    Retorna tots els incidents de la BD en format JSON.
    Endpoint: GET /api/incidents/
    """
    incidents_qs = SecurityIncident.objects.all().order_by('-detected_at')
    data = [
        {
            'id': inc.id,
            'title': inc.title,
            'description': inc.description,
            'severity': inc.severity,
            'detected_at': inc.detected_at.isoformat(),
            'creator': inc.creator.username,
        }
        for inc in incidents_qs
    ]
    return JsonResponse({'incidents': data, 'total': len(data)}, json_dumps_params={'ensure_ascii': False})


# ============================================
# VISTA ORIGINAL DEL PERFIL
# ============================================

@login_required
def perfil_usuari(request):
    return render(request, 'perfil.html')
