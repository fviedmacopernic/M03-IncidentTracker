#!/usr/bin/env python3
"""
==========================================================
P6 - PART 5: Test Appium per a IncidentTracker
==========================================================
Objectiu:
  - Obre l'App Android IncidentTracker a l'emulador
  - Clica el botó "Obtenir Incidents" (resource-id: copernic_button)
  - Verifica que l'incident amb el nom de l'alumne apareix a la UI

Cicle TDD:
  - RED  → Django aturat: AssertionError perquè no hi ha dades
  - GREEN → Django actiu: L'assert passa correctament

Prerequisits:
  pip install Appium-Python-Client

Ús:
  python test_appium_incidents.py
"""

import time
import unittest
from appium import webdriver
from appium.options import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# ─────────────────────────────────────────────
# CONFIGURACIÓ — Ajusta si cal
# ─────────────────────────────────────────────
APPIUM_SERVER = "http://127.0.0.1:4723"

# Text ÚNIC que has de posar al títol de l'incident creat des de l'Admin Django
# Ha de contenir el teu nom d'usuari de l'institut
INCIDENT_KEYWORD = "vonashura"  # ← CANVIA pel teu nom d'usuari del centre

APK_PATH = "/home/vonashura/GIT/M03/M03-IncidentTracker/appium_tests/IncidentTracker.apk"

CAPS = {
    "platformName": "Android",
    "appium:deviceName": "emulator-5554",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.example.incidenttracker",
    "appium:appActivity": ".MainActivity",
    "appium:app": APK_PATH,
    "appium:noReset": False,
    "appium:newCommandTimeout": 120,
}


class TestIncidentTrackerApp(unittest.TestCase):
    """
    Test d'integració de punta a punta:
    PostgreSQL → Django API → App Android (Emulador)
    """

    def setUp(self):
        """Inicia sessió Appium i obre l'app al emulador."""
        options = AppiumOptions()
        options.load_capabilities(CAPS)
        self.driver = webdriver.Remote(APPIUM_SERVER, options=options)
        self.driver.implicitly_wait(15)
        print("\n[APPIUM] Sessió iniciada. App carregant...")

    def tearDown(self):
        """Tanca la sessió Appium."""
        if self.driver:
            self.driver.quit()
            print("[APPIUM] Sessió tancada.")

    def test_incident_data_arrives_from_postgresql(self):
        """
        TEST PRINCIPAL: Verifica que el títol de l'incident creat
        a PART 1 (amb el nom d'usuari) és visible a la UI de l'app.

        Cicle TDD:
          RED  → Django off → AssertionError (no hi ha text de l'incident)
          GREEN → Django on  → Test PASSED
        """
        print(f"\n[TEST] Buscant botó amb ID: copernic_button")

        # PAS 1: Localitza i clica el botó de càrrega d'incidents
        try:
            btn = self.driver.find_element(
                AppiumBy.ID,
                "com.example.incidenttracker:id/copernic_button"
            )
        except Exception:
            # Fallback: busca per text si l'ID no coincideix
            btn = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@text,'Incident') or contains(@text,'Carreg') or contains(@text,'Load')]"
            )

        print(f"[TEST] Botó trobat! Clicant...")
        btn.click()

        # PAS 2: Espera que l'app rebi la resposta de la xarxa
        print(f"[TEST] Esperant resposta de 10.0.2.2:8000 (Django)...")
        time.sleep(10)

        # PAS 3: Captura el contingut visible de la pantalla
        page_source = self.driver.page_source

        # ─────────────────────────────────────────
        # ASSERT PRINCIPAL: El nom d'usuari ha d'aparèixer a la UI
        # ─────────────────────────────────────────
        print(f"\n[ASSERT] Verificant que '{INCIDENT_KEYWORD}' és visible a la UI...")
        self.assertIn(
            INCIDENT_KEYWORD,
            page_source,
            f"\n\n🔴 FAIL (RED): El text '{INCIDENT_KEYWORD}' NO apareix a la UI!\n"
            f"   → Comprova que Django estigui actiu (http://localhost:8000/api/incidents/)\n"
            f"   → Comprova que has creat l'incident amb '{INCIDENT_KEYWORD}' al títol\n"
            f"   → Comprova que l'emulador usa 10.0.2.2:8000 (no localhost)\n"
        )

        print(f"\n✅ GREEN: L'incident amb '{INCIDENT_KEYWORD}' s'ha verificat a la UI del mòbil!")
        print(f"   → Les dades han viatjat: PostgreSQL → Django API → App Android ✓")


if __name__ == "__main__":
    print("=" * 60)
    print("  P6 - TEST APPIUM: IncidentTracker End-to-End")
    print("=" * 60)
    print(f"  Keyword buscada: '{INCIDENT_KEYWORD}'")
    print(f"  Servidor Appium: {APPIUM_SERVER}")
    print("=" * 60)
    unittest.main(verbosity=2)
