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

# Función para guardar varios elementos por su tag
def guardar_varios_elementos_por_tag(soup, tag: str):
    
    # Busca los elementos en el contenido de la página
    elementos = soup.find_all(tag)
    return elementos

# Función para guardar varios elementos por su tag y clase
def guardar_varios_elementos_por_tag_y_atributo(soup, tag: str, atributo: str, valor_atributo: str):
    
    # Busca los elementos en el contenido de la página
    elementos = soup.find_all(tag, {atributo: valor_atributo})
    return elementos

# Funcion para obtener el texto de un elemento
def obtener_texto_elemento_buscado_por_tag(soup, tag: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag)
    return elemento.get_text(strip=True)

# Funcion para obtener el texto de un elemento buscado por tag y clase
def obtener_texto_elemento_buscado_por_tag_y_atributo(soup, tag: str, atributo: str, valor_atributo: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag, {atributo: valor_atributo})
    return elemento.get_text(strip=True)

# Funcion para obtener el atributo de un elemento buscado por tag
def obtener_atributo_elemento_buscado_por_tag(soup, tag: str, atributo_a_obtener: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag)
    return elemento[atributo_a_obtener]

# Funcion para obtener el atributo de un elemento buscado por tag y atributo
def obtener_atributo_elemento_buscado_por_tag_y_atributo(soup, tag: str, atributo: str, valor_atributo: str, atributo_a_obtener: str):
    
    # Busca el elemento en el contenido de la página
    elemento = soup.find(tag, {atributo: valor_atributo})
    return elemento[atributo_a_obtener]