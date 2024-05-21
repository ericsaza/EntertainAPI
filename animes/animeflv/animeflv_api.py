from enum import Enum
from bs4 import BeautifulSoup
from fastapi import Query
import requests
from scrapper.utils import obtener_contenido_url

# Enum de tipos de animes
class TipoAnime(str, Enum):
    tv = "tv"
    ova = "ova"
    pelicula = "movie"
    especial = "special"
    
# Enum de tipos de orden
class TipoOrden(str, Enum):
    defecto = "default"
    recientemente_actualizado = "updated"
    recientemente_agregado = "added"
    nombre = "title"
    calificacion = "rating"
# Enum de los posibles estados de un anime
class EstadoAnime(int, Enum):
    emision = 1
    finalizado = 2
    proximamente = 3

class AnimeflvAPI:
    
    # Endpoint para ver los últimos episodios de animes
    def episodios_recientes(self):
        
        # Entramos a la página donde scrapearemos la información

        # Parsea el contenido HTML de la página
        soup = obtener_contenido_url(f"https://www3.animeflv.net")
        
        # Buscamos todos los episodios recientes
        lista_animes = []
        for anime in soup.find("ul", {"class": "ListEpisodios"}).find_all("li"):
            titulo = anime.find("strong").text
            episodio = anime.find("span", {"class": "Capi"}).text.split(" ")[1]
            url = f'https://www3.animeflv.net{anime.find("a")["href"]}'
            image = f'https://www3.animeflv.net{anime.find("img")["src"]}'

            # Agregamos los datos a la lista
            lista_animes.append({"name": titulo, "episode": episodio, "image_src": image, "url": url})
        
        return {"message": "Últimos episodios de animes", "data": lista_animes, "code": 200}
    
    # Endpoint para ver los últimos animes añadidos
    def mostrar_ultimos_animes(self):
        
        # Parsea el contenido HTML de la página
        soup = obtener_contenido_url(f"https://www3.animeflv.net")
        
        # Buscamos todos los animes recientes
        lista_animes = []
        for anime in soup.find("ul", {"class": "ListAnimes"}).find_all("li"):
            titulo = anime.find("h3").text
            image = f'https://www3.animeflv.net{anime.find("img")["src"]}'
            sinopsis = anime.find_all("p")[1].text
            info_anime = f'https://www3.animeflv.net{anime.find_all("a")[1]["href"]}'
            anime_type = anime.find("span", {"class": "Type"}).text
            url_api = anime.find_all("a")[1]["href"].replace("/anime/", "/buscar_anime?anime_a_buscar=")
            rating = anime.find("span", {"class": "Vts fa-star"}).text
            
            # Agregamos los datos a la lista
            lista_animes.append({"title": titulo, "image_src": image, "sinopsis": sinopsis, "view_info": info_anime, "type": anime_type, "url_api": url_api, "puntuacion": rating})
        
        return {"message": "Últimos animes añadidos", "data": lista_animes, "code": 200}
    
    def ver_directorio_animes(self,
        pagina: int = Query(1, description="Número de la página que deseas ver."),
        tipo: TipoAnime = Query(None, description="Tipo de anime para filtrar los resultados (TV = tv , OVA = ova, Película = movie, Especial = special)."),
        orden: TipoOrden = Query(TipoOrden.defecto, description="Criterio de ordenación de los resultados (defecto = default, recientemente actualizado = updated, recientemente agregado = added, nombre = title, calificación = rating)."),
        estado: EstadoAnime = Query(None, description="Estado del anime para filtrar los resultados (emisión = 1, finalizado = 2, próximamente = 3).")
    ):
    
        # Entramos a la página donde scrapearemos la información del directorio
        url = f"https://www3.animeflv.net/browse?page={pagina}{f"&type%5B%5D={tipo.value}" if tipo != None else ""}{f"&order={orden.value}" if orden != TipoOrden.defecto else ""}{f"&status={estado.value}" if estado != None else ""}"
        print(url)
        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url)

        # Parsea el contenido HTML de la página
        soup = BeautifulSoup(response.content, "lxml")
        
        # Buscamos todos los animes recientes
        lista_animes = []
        
        # Recorremos los animes
        for anime in soup.find("ul", {"class": "ListAnimes"}).find_all("li"):
            titulo = anime.find("h3").text
            image = anime.find("img")["src"]
            sinopsis = anime.find_all("p")[1].text
            anime_type = anime.find("span", {"class": "Type"}).text
            url_api = anime.find("a")["href"].replace("/anime/", "/buscar_anime?anime_a_buscar=")
            rating = anime.find("span", {"class": "Vts fa-star"}).text

            # Agregamos los datos a la lista
            lista_animes.append({"title": titulo, "image_src": image, "sinopsis": sinopsis, "type": anime_type, "url_api": url_api, "puntuacion": rating})
        
        return {"message": "Directorio de animes", "data": lista_animes, "pagination": [{"prev_page": f"/directorio-animes?pagina={pagina - 1}" if pagina > 1 else None}, {"next_page": f"/directorio-animes?pagina={pagina + 1}"}], "code": 200}
