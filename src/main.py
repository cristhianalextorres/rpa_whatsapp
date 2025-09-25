import pandas as pd
import requests
from io import BytesIO
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsAppSender:
    def __init__(self, excel_url):
        self.excel_url = excel_url
        self.driver = None
        self.data = None

    def download_excel(self):
        """Descarga y carga la hoja de cálculo"""
        response = requests.get(self.excel_url)
        self.data = pd.read_excel(BytesIO(response.content))
        print("✅ Hoja de cálculo cargada correctamente")

    def initialize_driver(self):
        """Inicializa el navegador Chrome"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://web.whatsapp.com")
        input("Escanea el código QR y presiona ENTER para continuar...")
        print("✅ Navegador inicializado correctamente")

    def send_message(self, number, message):
        """Envía un mensaje a un número específico"""
        try:
            # Codificar saltos de línea para URL
            message = message.replace("\n", "%0A")
            url = f"https://web.whatsapp.com/send?phone=57{number}&text={message}"
            self.driver.get(url)

            # Esperar que aparezca el botón de enviar y hacer clic
            send_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='wds-ic-send-filled']"))
            )
            send_button.click()
            print(f"✅ Mensaje enviado a {number}")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"❌ No se pudo enviar a {number}: {e}")
            return False

    def process_all_messages(self):
        """Procesa y envía todos los mensajes de la hoja de cálculo"""
        for index, row in self.data.iterrows():
            numero = str(row['Numero'])
            mensaje = row['Mensaje']
            self.send_message(numero, mensaje)

    def close(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            print("✅ Navegador cerrado correctamente")

def main():
    # URL de la hoja de cálculo
    excel_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR9hZ3mVP7OUaKJfArCXFAnWL8j5OZdqikWo4548vH4fD2l_8e2e7nU5hiKiR2fdmQJA3CLGPlTxsiZ/pub?output=xlsx"
    
    # Crear instancia del sender
    sender = WhatsAppSender(excel_url)
    
    try:
        # Ejecutar el proceso completo
        sender.download_excel()
        sender.initialize_driver()
        sender.process_all_messages()
    finally:
        # Asegurar que el navegador se cierre al finalizar
        sender.close()

if __name__ == "__main__":
    main()
