# Importamos BeautifulSoup
from bs4 import BeautifulSoup
import requests

# Función para obtener el contenido de una página web
def obtener_contenido_url(url: str):
    # Realiza una solicitud HTTP GET a la URL
    response = requests.get(url)

    # Parsea el contenido HTML de la página
    soup = BeautifulSoup(response.content, "lxml")
    
    return soup