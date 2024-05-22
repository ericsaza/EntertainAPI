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

# Función para guardar un elemento por su tag
def guardar_elemento_por_tag(soup, tag: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag)
    return elemento


# Función para guardar un elemento por su tag y clase
def guardar_elemento_por_tag_y_atributo(soup, tag: str, atributo: str, valor_atributo: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag, {atributo: valor_atributo})
    return elemento