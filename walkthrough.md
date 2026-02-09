# Walkthrough - Pràctica 3: Auditoria Forense

## Resum de la Implementació

S'ha implementat completament l'exercici d'auditoria de seguretat per a IncidentTracker, incloent vulnerabilitats intencionades, versions segures, tests automatitzats i documentació completa.

![Pàgina de Perfil amb Navegació](/home/vonashura/.gemini/antigravity/brain/aafc1d4e-42af-405a-8cac-927b602572b6/profile_page_navigation_1770661836394.png)

*Captura de la pàgina de perfil mostrant el menú de navegació amb enllaços a totes les vistes vulnerables i segures.*

## Components Implementats

### 1. Model de Dades

**Modificacions a [`core/models.py`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/core/models.py)**

- Afegit camp `creator` (ForeignKey a User) per habilitar control d'accés basat en propietari
- Migració creada i aplicada correctament

### 2. Vistes Vulnerables

**Implementades a [`core/views.py`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/core/views.py)**

| Vista | Vulnerabilitat | Apartat |
|-------|----------------|---------|
| `cerca_resultats_vulnerable` | SQL Injection | 2 & 3 |
| `actualitzar_email_vulnerable` | SQLi + Privilege Escalation | 4 |
| `incident_detall_vulnerable` | IDOR | 7 |
| `incident_llista` | XSS (amb `\|safe`) | 9 |

### 3. Vistes Segures

| Vista | Protecció | Apartat |
|-------|-----------|---------|
| `cerca_resultats_segura` | ORM amb prepared statements | 6 |
| `actualitzar_email_segur` | ORM amb `.save()` | 6 |
| `incident_detall_segur` | Control d'accés per `creator` | 8 |

### 4. Templates

Creades 7 plantilles HTML:

- [`cerca.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/cerca.html) - Formulari de cerca
- [`cerca_resultats.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/cerca_resultats.html) - Resultats vulnerables
- [`cerca_resultats_segura.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/cerca_resultats_segura.html) - Resultats segurs
- [`actualitzar_email.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/actualitzar_email.html) - Formulari amb payload d'exemple
- [`incident_detall.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/incident_detall.html) - Detall d'incident
- [`incident_llista.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/incident_llista.html) - Llista amb XSS
- [`perfil.html`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/templates/perfil.html) - Actualitzat amb navegació

### 5. URLs

**Configurades a [`config/urls.py`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/config/urls.py)**

```
/cerca/                      → Formulari de cerca
/cerca/resultats/            → Cerca vulnerable (SQLi)
/actualitzar-email/          → Actualització vulnerable (Privilege Escalation)
/incident/<id>/              → Detall vulnerable (IDOR)
/incidents/                  → Llista amb XSS
/secure/cerca/resultats/     → Cerca segura
/secure/actualitzar-email/   → Actualització segura
/secure/incident/<id>/       → Detall segur
```

### 6. Tests Automatitzats (TDD)

**Implementats a [`core/tests.py`](file:///home/vonashura/GIT/M03/M03-IncidentTracker/core/tests.py)**

| Test | Objectiu | Estat Inicial |
|------|----------|---------------|
| `test_privilege_escalation_via_email_update` | Detectar escalada de privilegis | ❌ FAIL (correcte) |
| `test_sql_injection_in_search` | Detectar SQLi en cerca | ❌ FAIL |
| `test_idor_access_control` | Detectar IDOR | ❌ FAIL |
| `test_xss_protection` | Detectar XSS | ❌ FAIL |
| `test_secure_search_with_orm` | Verificar cerca segura | ✅ OK |
| `test_secure_incident_detail` | Verificar detall segur | ✅ OK |

**Verificació del Fail-First (APARTAT 5):**

```bash
python3 manage.py test core.tests.SecurityTestCase.test_privilege_escalation_via_email_update
```

Resultat: **FAIL** amb missatge:
```
VULNERABILITAT DETECTADA: L'usuari ha esdevingut superusuari via SQL injection!
```

## Manual de Comandes

S'ha creat un document complet amb totes les comandes necessàries per fer les captures de pantalla:

**[`manual_comandes.md`](file:///home/vonashura/.gemini/antigravity/brain/aafc1d4e-42af-405a-8cac-927b602572b6/manual_comandes.md)**

Aquest manual inclou:

- **APARTAT 1:** Comandes Docker per crear usuari amb password en text pla
- **APARTAT 2:** Identificació de la línia vulnerable
- **APARTAT 3:** Payload SQLi: `' OR '1'='1`
- **APARTAT 4:** Payload privilege escalation: `test@test.com', is_superuser = TRUE WHERE id = X; --`
- **APARTAT 5:** Comanda per executar test (FAIL)
- **APARTAT 6:** Comanda per executar test després de corregir (OK)
- **APARTAT 7:** Procediment per IDOR
- **APARTAT 8:** Verificació de control d'accés
- **APARTAT 9:** Payload XSS: `<script>alert(document.cookie)</script>`
- **APARTAT 10:** Com activar DEBUG i generar error

## Estructura de Fitxers Modificats/Creats

```
M03-IncidentTracker/
├── core/
│   ├── models.py                    [MODIFICAT] +1 camp
│   ├── views.py                     [MODIFICAT] +161 línies
│   ├── tests.py                     [MODIFICAT] +218 línies
│   └── migrations/
│       └── 0002_securityincident_creator.py  [NOU]
├── templates/
│   ├── cerca.html                   [NOU]
│   ├── cerca_resultats.html         [NOU]
│   ├── cerca_resultats_segura.html  [NOU]
│   ├── actualitzar_email.html       [NOU]
│   ├── incident_detall.html         [NOU]
│   ├── incident_llista.html         [NOU]
│   └── perfil.html                  [MODIFICAT] +navegació
└── config/
    └── urls.py                      [MODIFICAT] +8 rutes
```

## Com Utilitzar

### 1. Iniciar el Servidor

```bash
cd /home/vonashura/GIT/M03/M03-IncidentTracker
source .venv/bin/activate
python3 manage.py runserver
```

### 2. Accedir al Perfil

1. Ves a: `http://127.0.0.1:8000/accounts/login/`
2. Login amb `admin` o `analista1`
3. Seràs redirigit a: `http://127.0.0.1:8000/perfil/`

### 3. Navegació

Des del perfil pots accedir a:

- **Vulnerabilitats:** Cerca SQLi, Actualitzar Email, Llista XSS
- **Versions Segures:** Cerca ORM, Actualitzar Email Segur

### 4. Seguir el Manual

Obre [`manual_comandes.md`](file:///home/vonashura/.gemini/antigravity/brain/aafc1d4e-42af-405a-8cac-927b602572b6/manual_comandes.md) i segueix les instruccions per a cada apartat, fent captures de pantalla segons s'indica.

## Punts Clau per a l'Informe

### Diferència entre Vulnerable i Segur

**Vulnerable (SQL Raw):**
```python
sql = f"SELECT * FROM table WHERE field = '{user_input}'"
cursor.execute(sql)  # ⚠️ PERILL
```

**Segur (ORM):**
```python
Model.objects.filter(field=user_input)  # ✅ SEGUR
```

### Per què l'ORM és Segur?

Django utilitza **prepared statements** (queries parametritzades):

```sql
-- L'ORM genera:
SELECT * FROM table WHERE field = %s
-- I passa user_input com a paràmetre separat
```

Això impedeix que l'input de l'usuari sigui interpretat com a codi SQL.

### Principi de Privilegi Mínim (IDOR)

```python
# Vulnerable
incident = get_object_or_404(SecurityIncident, id=id)

# Segur
incident = get_object_or_404(SecurityIncident, id=id, creator=request.user)
```

Només retorna l'objecte si pertany a l'usuari actual.

### Output Encoding (XSS)

```django
{{ incident.title }}           {# ✅ Escapat automàticament #}
{{ incident.title|safe }}      {# ⚠️ NO escapat, permet XSS #}
```

## Pregunta Final de l'Auditor

**Si un atacant aconsegueix el `SECRET_KEY`:**

1. **CSRF Bypass:** Pot forjar tokens CSRF vàlids
2. **Session Hijacking:** Pot crear sessions falses
3. **Cookie Tampering:** Pot modificar cookies signades
4. **Password Reset Tokens:** Pot generar tokens de reset vàlids

**Atacs més greus:**
- **Apartat 4 (Privilege Escalation):** Més fàcil si pot forjar sessions d'admin
- **Apartat 9 (XSS):** Pot combinar XSS amb session hijacking
- **Tots els apartats:** Pot autenticar-se com qualsevol usuari sense password

## Estat Final

✅ **Tots els components implementats**  
✅ **Tests funcionant (Fail-First verificat)**  
✅ **Manual complet amb comandes**  
✅ **Navegació funcional**  
✅ **Llest per fer captures**

El projecte està preparat per a l'avaluació. Segueix el `manual_comandes.md` per generar totes les evidències necessàries.
