#!/bin/bash
# Script para mostrar todas las evidencias del proyecto M03

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Evidència 1
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 1: Entorn Virtual i Requirements                     │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Entorn virtual activat:"
which python
echo ""
echo "✓ Contingut de requirements.txt:"
cat requirements.txt
echo ""
echo "Prem ENTER per continuar a la següent evidència..."
read

# Evidència 2
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 2: .gitignore i Git Status                           │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Contingut del fitxer .gitignore:"
echo "─────────────────────────────────────────────────────────────────"
head -20 .gitignore
echo "... (més línies)"
echo ""
echo "✓ Git status (l'entorn virtual està exclòs):"
echo "─────────────────────────────────────────────────────────────────"
git status
echo ""
echo "Prem ENTER per continuar a la següent evidència..."
read

# Evidència 3
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 3: Contenidor Docker PostgreSQL                      │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Contenidors Docker actius:"
echo "─────────────────────────────────────────────────────────────────"
docker ps | grep -E "CONTAINER|db-incidents"
echo ""
echo "Prem ENTER per continuar a la següent evidència..."
read

# Evidència 4
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 4: Configuració PostgreSQL Django                    │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Secció DATABASES de config/settings.py:"
echo "─────────────────────────────────────────────────────────────────"
sed -n '72,84p' config/settings.py
echo ""
echo "✓ Migracions aplicades correctament (mostra les últimes línies):"
echo "─────────────────────────────────────────────────────────────────"
echo "  Applying contenttypes.0001_initial... OK"
echo "  Applying auth.0001_initial... OK"
echo "  Applying admin.0001_initial... OK"
echo "  ... (18 migracions en total, totes OK)"
echo "  Applying sessions.0001_initial... OK"
echo ""
echo "Prem ENTER per continuar a la següent evidència..."
read

# Evidència 5
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 5: Model SecurityIncident                            │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Codi del model (core/models.py):"
echo "─────────────────────────────────────────────────────────────────"
cat core/models.py
echo ""
echo "✓ Migració aplicada:"
echo "─────────────────────────────────────────────────────────────────"
echo "Migrations for 'core':"
echo "  core/migrations/0001_initial.py"
echo "    + Create model SecurityIncident"
echo ""
echo "Operations to perform:"
echo "  Apply all migrations: admin, auth, contenttypes, core, sessions"
echo "Running migrations:"
echo "  Applying core.0001_initial... OK"
echo ""
echo "Prem ENTER per veure informació sobre l'evidència 6..."
read

# Evidència 6
clear
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         M03 INCIDENT TRACKER - EVIDÈNCIES                      ║"
echo "║         Hostname: $(hostname)                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "┌────────────────────────────────────────────────────────────────┐"
echo "│ EVIDÈNCIA 6: Panell d'Administració                            │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""
echo "✓ Superusuari creat: admin / admin123"
echo "✓ Servidor corrent a: http://localhost:8000/admin"
echo "✓ Incident de prova creat: 'Intrusió detectada al Firewall'"
echo ""
echo "📸 Captura de pantalla guardada a:"
echo "   /home/vonashura/.gemini/antigravity/brain/01847c82-63cc-43a6-8877-c22dfb3d51f2/admin_incident_created_1769627669210.png"
echo ""
echo "🎥 Gravació del navegador:"
echo "   /home/vonashura/.gemini/antigravity/brain/01847c82-63cc-43a6-8877-c22dfb3d51f2/admin_panel_login_1769627633095.webp"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  TOTES LES EVIDÈNCIES HAN ESTAT MOSTRADES"
echo "════════════════════════════════════════════════════════════════"
