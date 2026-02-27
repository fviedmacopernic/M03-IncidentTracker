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
    }

    post {
        success {
            echo '✅ AUDITORIA COMPLETADA: Tots els tests de seguretat RBAC han passat!'
        }
        failure {
            echo '🚨 ALERTA DE SEGURETAT: Els tests RBAC han fallat! Desplegament bloquejat!'
        }
        always {
            echo "=== FI DE LA PIPELINE D'AUDITORIA DEVSECOPS ==="
        }
    }
}
