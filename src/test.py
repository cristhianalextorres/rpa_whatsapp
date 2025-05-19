from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Iniciar Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abrir WhatsApp Web
driver.get("https://web.whatsapp.com")

# Mantener abierto hasta que cierres manualmente
input("Presiona ENTER para cerrar...")
driver.quit()
