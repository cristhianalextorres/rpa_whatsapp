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

# 1. Descargar hoja de cálculo pública
url_excel = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR9hZ3mVP7OUaKJfArCXFAnWL8j5OZdqikWo4548vH4fD2l_8e2e7nU5hiKiR2fdmQJA3CLGPlTxsiZ/pub?output=xlsx"
response = requests.get(url_excel)
data = pd.read_excel(BytesIO(response.content))

# 2. Iniciar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://web.whatsapp.com")

input("Escanea el código QR y presiona ENTER para continuar...")

# 3. Recorrer cada estudiante y enviar mensaje
for index, row in data.iterrows():
    numero = str(row['Numero'])
    mensaje = row['Mensaje'].replace("\n", "%0A")  # Codificar saltos de línea para URL

    # Crear URL para enviar mensaje
    url = f"https://web.whatsapp.com/send?phone=57{numero}&text={mensaje}"  # Asegúrate del código del país (57 = Colombia)
    driver.get(url)

# 2. Esperar a que cargue y hacer clic en enviar
    try:
        # Esperar que aparezca el botón de enviar y hacer clic
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_button.click()
        print(f"✅ Mensaje enviado a {numero}")
        time.sleep(5)
    except Exception as e:
        print(f"❌ No se pudo enviar a {numero}: {e}")
        continue
driver.quit()
