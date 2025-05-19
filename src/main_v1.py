import pandas as pd
import requests
from io import BytesIO

# URL directa del archivo XLSX publicado
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR9hZ3mVP7OUaKJfArCXFAnWL8j5OZdqikWo4548vH4fD2l_8e2e7nU5hiKiR2fdmQJA3CLGPlTxsiZ/pub?output=xlsx"

# Descargar el archivo
response = requests.get(url)
response.raise_for_status()  # Lanza error si falla la descarga

# Leer el contenido con pandas
excel_data = pd.read_excel(BytesIO(response.content))

# Mostrar los datos
print(excel_data.head())

