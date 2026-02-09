from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import SecurityIncident

class SecurityTestCase(TestCase):
    """
    Tests de seguretat per detectar vulnerabilitats.
    Aquests tests segueixen la metodologia TDD amb Fail-First.
    """
    
    def setUp(self):
        """Configuració inicial per a cada test"""
        # Crear usuaris de prova
        self.user1 = User.objects.create_user(
            username='analista1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='analista2',
            password='password123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        
        # Crear incidents de prova
        self.incident1 = SecurityIncident.objects.create(
            title='Incident de l\'Analista 1',
            description='Descripció incident 1',
            severity='HIGH',
            creator=self.user1
        )
        self.incident2 = SecurityIncident.objects.create(
            title='Incident de l\'Analista 2',
            description='Descripció incident 2',
            severity='MEDIUM',
            creator=self.user2
        )
        
        # Client per fer requests
        self.client = Client()
    
    # ============================================
    # APARTAT 5: TEST DE PRIVILEGE ESCALATION
    # ============================================
    
    def test_privilege_escalation_via_email_update(self):
        """
        APARTAT 5: Test que detecta la vulnerabilitat de privilege escalation.
        
        Aquest test FALLARÀ inicialment perquè la vista vulnerable permet
        modificar is_superuser mitjançant SQL injection.
        
        Després de corregir amb l'ORM (APARTAT 6), aquest test PASSARÀ.
        """
        # Login com a usuari normal
        self.client.login(username='analista1', password='password123')
        
        # Verificar que inicialment NO és superusuari
        self.user1.refresh_from_db()
        self.assertFalse(self.user1.is_superuser, "L'usuari no hauria de ser superusuari inicialment")
        
        # Payload maliciós per escalada de privilegis
        # PostgreSQL requereix TRUE/FALSE per booleans, no 1/0
        payload = f"test@test.com', is_superuser = TRUE WHERE id = {self.user1.id}; --"
        
        # Enviar payload a la vista vulnerable
        response = self.client.post('/actualitzar-email/', {
            'email': payload
        })
        
        # Refrescar l'usuari des de la BD
        self.user1.refresh_from_db()
        
        # ⚠️ AQUEST ASSERT FALLARÀ amb la versió vulnerable
        # ✅ AQUEST ASSERT PASSARÀ amb la versió segura (ORM)
        self.assertFalse(
            self.user1.is_superuser,
            "VULNERABILITAT DETECTADA: L'usuari ha esdevingut superusuari via SQL injection!"
        )
    
    # ============================================
    # TEST DE SQL INJECTION EN CERCA
    # ============================================
    
    def test_sql_injection_in_search(self):
        """
        Test que verifica que la cerca no retorna incidents d'altres usuaris
        quan s'utilitza un payload SQLi.
        """
        # Login com a analista1
        self.client.login(username='analista1', password='password123')
        
        # Payload SQLi per veure tots els incidents
        payload = "' OR '1'='1"
        
        # Fer cerca amb payload maliciós
        response = self.client.get('/cerca/resultats/', {'q': payload})
        
        # La versió vulnerable retornarà incidents de tots els usuaris
        # La versió segura només retornarà incidents de l'usuari actual
        
        # Aquest test passa si NO es troben incidents d'altres usuaris
        content = response.content.decode('utf-8')
        
        # Verificar que NO apareix l'incident de l'analista2
        self.assertNotIn(
            'Incident de l\'Analista 2',
            content,
            "VULNERABILITAT: La cerca retorna incidents d'altres usuaris!"
        )
    
    # ============================================
    # TEST DE IDOR (INSECURE DIRECT OBJECT REFERENCE)
    # ============================================
    
    def test_idor_access_control(self):
        """
        Test que verifica que un usuari NO pot accedir a incidents d'altres usuaris
        modificant la ID a la URL.
        """
        # Login com a analista1
        self.client.login(username='analista1', password='password123')
        
        # Intentar accedir a l'incident de l'analista2
        response = self.client.get(f'/incident/{self.incident2.id}/')
        
        # La versió vulnerable retornarà 200 OK
        # La versió segura retornarà 404 Not Found
        
        # Aquest test passa si retorna 404
        self.assertEqual(
            response.status_code,
            404,
            f"VULNERABILITAT IDOR: L'usuari pot accedir a incidents aliens! Status: {response.status_code}"
        )
    
    # ============================================
    # TEST DE XSS
    # ============================================
    
    def test_xss_protection(self):
        """
        Test que verifica que els scripts no s'executen (són escapats).
        
        Nota: Aquest test verifica l'escapament HTML, però no pot detectar
        si el navegador executarà el JavaScript. Per això cal fer proves manuals.
        """
        # Crear incident amb payload XSS
        xss_incident = SecurityIncident.objects.create(
            title='<script>alert("XSS")</script>',
            description='Test XSS',
            severity='LOW',
            creator=self.user1
        )
        
        # Login i accedir a la llista
        self.client.login(username='analista1', password='password123')
        response = self.client.get('/incidents/')
        
        content = response.content.decode('utf-8')
        
        # Amb |safe, el script NO estarà escapat (VULNERABLE)
        # Sense |safe, el script estarà escapat com &lt;script&gt; (SEGUR)
        
        # Aquest test detecta si el filtre |safe està actiu
        if '<script>alert("XSS")</script>' in content:
            self.fail("VULNERABILITAT XSS: El filtre |safe permet execució de scripts!")
    
    # ============================================
    # TEST DE VERSIONS SEGURES
    # ============================================
    
    def test_secure_search_with_orm(self):
        """
        Test que verifica que la cerca segura només retorna incidents propis.
        """
        # Login com a analista1
        self.client.login(username='analista1', password='password123')
        
        # Fer cerca amb payload SQLi a la versió segura
        payload = "' OR '1'='1"
        response = self.client.get('/secure/cerca/resultats/', {'q': payload})
        
        content = response.content.decode('utf-8')
        
        # Verificar que només apareixen incidents de l'usuari actual
        self.assertIn('Incident de l\'Analista 1', content)
        self.assertNotIn('Incident de l\'Analista 2', content)
    
    def test_secure_incident_detail(self):
        """
        Test que verifica que la vista segura de detall aplica control d'accés.
        """
        # Login com a analista1
        self.client.login(username='analista1', password='password123')
        
        # Intentar accedir a incident aliè amb la versió segura
        response = self.client.get(f'/secure/incident/{self.incident2.id}/')
        
        # Ha de retornar 404
        self.assertEqual(response.status_code, 404)
        
        # Accedir al propi incident ha de funcionar
        response = self.client.get(f'/secure/incident/{self.incident1.id}/')
        self.assertEqual(response.status_code, 200)
