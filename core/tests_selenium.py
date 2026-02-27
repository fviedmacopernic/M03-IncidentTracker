from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import os


class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']  # Càrrega de dades (Punt 2.2.2)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")  # mode Headless (Punt 2.2.1)
        # Suport per Firefox instal·lat via Snap (Ubuntu)
        firefox_snap = "/snap/firefox/current/usr/lib/firefox/firefox"
        if os.path.exists(firefox_snap):
            opts.binary_location = firefox_snap
        service = Service(executable_path="/snap/bin/geckodriver")
        cls.selenium = WebDriver(service=service, options=opts)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        # PUNT 2.2.3: Login amb 'analista1'
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("password123")
        self.selenium.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Intentar forçar URL d'admin
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

        # ASSERT de Seguretat (Punt 2.2.3):
        # Si l'analista té is_staff=True, Django li mostraria el panell admin
        # i el títol seria "Site administration | Django site admin".
        # El test FALLA (RED) si l'analista TÉ accés al panel d'admin.
        # El test PASSA (GREEN) si l'analista NO té accés (is_staff=False).
        self.assertNotEqual(
            self.selenium.title,
            "Site administration | Django site admin",
            "VULNERABILITAT RBAC: L'analista1 ha accedit al panell d'administació!"
        )
