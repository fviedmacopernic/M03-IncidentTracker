pipeline {
    agent any

    environment {
        // Directori de l'entorn virtual de Python
        VENV_DIR = "${WORKSPACE}/.venv"
        // Usar SQLite per a CI/CD (no necessita Postgres)
        DATABASE_URL = "sqlite:///db_jenkins.sqlite3"
        DEBUG = "True"
        MOZ_HEADLESS = "1"
    }

    stages {
        stage('📥 Checkout') {
            steps {
                echo "=== CLONANT REPOSITORI ==="
                checkout scm
            }
        }

        stage('🐍 Configurar Python') {
            steps {
                echo "=== CONFIGURANT ENTORN PYTHON ==="
                sh '''
                    python3 --version
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('🦊 Verificar Firefox i Geckodriver') {
            steps {
                echo "=== VERIFICANT FIREFOX I GECKODRIVER ==="
                sh '''
                    firefox --version || firefox-esr --version
                    geckodriver --version
                '''
            }
        }

        stage('🗄️ Migracions de BD') {
            steps {
                echo "=== APLICANT MIGRACIONS (SQLite) ==="
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python manage.py migrate --run-syncdb
                '''
            }
        }

        stage('🔒 Tests de Seguretat RBAC (Selenium)') {
            steps {
                echo "=== EXECUTANT TESTS DE SEGURETAT RBAC ==="
                sh '''
                    . ${VENV_DIR}/bin/activate
                    MOZ_HEADLESS=1 python manage.py test core.tests_selenium --verbosity=2
                '''
            }
        }

        stage('✅ Tests Unitaris') {
            steps {
                echo "=== EXECUTANT TOTS ELS TESTS ==="
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python manage.py test core --verbosity=2
                '''
            }
        }

        stage('📱 Test API JSON (P6)') {
            steps {
                echo "=== VERIFICANT ENDPOINT API /api/incidents/ ==="
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Llancem el servidor Django en background
                    python manage.py runserver 0.0.0.0:9090 &
                    DJANGO_PID=$!
                    sleep 5

                    # Test: L'endpoint ha de respondre amb JSON vàlid
                    RESPONSE=$(curl -s http://localhost:9090/api/incidents/)
                    echo "Resposta API: $RESPONSE"

                    # Matem el servidor
                    kill $DJANGO_PID 2>/dev/null || true

                    # Validem que la resposta conté clau "incidents"
                    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
assert 'incidents' in data, 'ERROR: La clau incidents no existeix al JSON!'
assert 'total' in data, 'ERROR: La clau total no existeix al JSON!'
print(f'OK: API retorna {data[\"total\"]} incidents correctament.')
"
                '''
            }
        }

        stage('⛈️ Simulació Fallada Appium (P6 - Storm Evidence)') {
            steps {
                echo "=== SIMULANT FALLADA DEL TEST APPIUM ==="
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Aquest stage simula el test Appium sense emulador
                    # per provocar la icona ⛈️ (Storm) al dashboard de Jenkins
                    echo "INFO: En un entorn real, aqui s'executaria:"
                    echo "  python appium_tests/test_appium_incidents.py"
                    echo ""
                    echo "STATUS: Emulador Android no disponible al contenidor Jenkins."
                    echo "        Consulta: http://localhost:4723 (Appium Server)"
                    # Retorna exit 1 per provocar el Weather 'Storm' al dashboard
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo '✅ AUDITORIA COMPLETADA: Tots els tests de seguretat RBAC han passat!'
        }
        failure {
            echo '🚨 ALERTA DE SEGURETAT: Un o més tests han fallat!'
            echo '⛈️  STORM: El dashboard de Jenkins mostra icona de tempesta.'
            echo '   → Significat: >50% de les darreres execucions han fallat.'
            echo '   → Acció: Revisar els logs del stage "Simulació Fallada Appium".'
        }
        always {
            echo "=== FI DE LA PIPELINE D'AUDITORIA DEVSECOPS P6 ==="
        }
    }
}
