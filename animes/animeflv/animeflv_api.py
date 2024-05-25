from enum import Enum
from bs4 import BeautifulSoup
from fastapi import Query
import requests
from utils.scrap_utils import *

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
    
    def info_endpoint(self):
        return {
            "message": "Endpoint para ver la información de la API de AnimeFLV.",
            "description": "Este endpoint te mostrará la información de la API de AnimeFLV, incluyendo los endpoints disponibles, la documentación de la API y el código de respuesta.",
            "endpoints": { 
                        "episodios_recientes": "/api/anime/animeflv/episodios-recientes",
                        "ultimos_animes": "/api/anime/animeflv/ultimos-animes",
                        "directorio_animes": "/api/anime/animeflv/directorio-animes?pagina=1",
                        "buscar_anime": "/api/anime/animeflv/buscar-anime?anime_a_buscar=sword%20art%20online",
                        "ver_info_anime": "/api/anime/animeflv/info-anime?anime_a_buscar=sword%20art%20online",
                    },
            "other_anime_endpoints": {
                "MyAnimeList": "/api/anime/myanimelist",
            },
            "documentation": {"swagger": "/docs", "doc": "/redoc"},
            "code": 200,
        }
    
    # Endpoint para ver los últimos episodios de animes
    def episodios_recientes(self):

        # Parsea el contenido HTML de la página
        soup = obtener_contenido_url(f"https://www3.animeflv.net")
        
        # Buscamos todos los episodios recientes
        lista_animes = []
        for anime in soup.find("ul", {"class": "ListEpisodios"}).find_all("li"):
            titulo = obtener_texto_elemento_buscado_por_tag(anime, "strong")
            episodio = obtener_texto_elemento_buscado_por_tag_y_atributo(anime, "span", "class", "Capi").split(" ")[1]
            url = f'https://www3.animeflv.net{obtener_atributo_elemento_buscado_por_tag(anime, "a", "href")}'
            image = f'https://www3.animeflv.net{obtener_atributo_elemento_buscado_por_tag(anime, "img", "src")}'

            # Agregamos los datos a la lista
            lista_animes.append({"title": titulo, "episode": episodio, "image_src": image, "url": url})
        
        return {"message": "Últimos episodios de animes", "data": lista_animes, "code": 200}
    
    # Endpoint para ver los últimos animes añadidos
    def mostrar_ultimos_animes(self):
        
        # Parsea el contenido HTML de la página
        soup = obtener_contenido_url(f"https://www3.animeflv.net")
        
        # Buscamos todos los animes recientes
        lista_animes = []
        for anime in soup.find("ul", {"class": "ListAnimes"}).find_all("li"):
            titulo = obtener_texto_elemento_buscado_por_tag(anime, "h3")
            image = f'https://www3.animeflv.net{obtener_atributo_elemento_buscado_por_tag(anime, "img", "src")}'
            sinopsis = guardar_varios_elementos_por_tag(anime, "p")[1].text
            info_anime = f'https://www3.animeflv.net{anime.find_all("a")[1]["href"]}'
            anime_type = obtener_texto_elemento_buscado_por_tag_y_atributo(anime, "span", "class", "Type")
            url_api = guardar_varios_elementos_por_tag(anime, "a")[1]["href"].replace("/anime/", "/api/anime/animeflv/info-anime?anime_a_buscar=")
            rating = obtener_texto_elemento_buscado_por_tag_y_atributo(anime, "span", "class", "Vts fa-star")
            
            # Agregamos los datos a la lista
            lista_animes.append({"title": titulo, "image_src": image, "sinopsis": sinopsis, "type": anime_type, "score": rating, "animeflv_info": info_anime, "url_api": url_api})
        
        return {"message": "Últimos animes añadidos", "data": lista_animes, "code": 200}
    
    def ver_directorio_animes(self,
        pagina: int = Query(..., example=1, description="Número de la página que deseas ver."),
        tipo: TipoAnime = Query(None, description="Tipo de anime para filtrar los resultados (TV = tv , OVA = ova, Película = movie, Especial = special)."),
        orden: TipoOrden = Query(TipoOrden.defecto, description="Criterio de ordenación de los resultados (defecto = default, recientemente actualizado = updated, recientemente agregado = added, nombre = title, calificación = rating)."),
        estado: EstadoAnime = Query(None, description="Estado del anime para filtrar los resultados (emisión = 1, finalizado = 2, próximamente = 3).")
    ):
    
        # Entramos a la página donde scrapearemos la información del directorio
        soup = obtener_contenido_url(f"https://www3.animeflv.net/browse?page={pagina}{f"&type%5B%5D={tipo.value}" if tipo != None else ""}{f"&order={orden.value}" if orden != TipoOrden.defecto else ""}{f"&status={estado.value}" if estado != None else ""}")
        
        # Buscamos todos los animes recientes
        lista_animes = []
        
        # Recorremos los animes
        for anime in soup.find("ul", {"class": "ListAnimes"}).find_all("li"):
            titulo = anime.find("h3").text
            image = anime.find("img")["src"]
            sinopsis = anime.find_all("p")[1].text
            anime_type = anime.find("span", {"class": "Type"}).text
            animeflv_info = f'https://www3.animeflv.net{anime.find("a")["href"]}'
            url_api = anime.find("a")["href"].replace("/anime/", "/api/anime/animeflv/buscar-anime?anime_a_buscar=")
            rating = anime.find("span", {"class": "Vts fa-star"}).text

            # Agregamos los datos a la lista
            lista_animes.append({"title": titulo, "image_src": image, "sinopsis": sinopsis, "type": anime_type, "score": rating, "animeflv_info": animeflv_info, "url_api": url_api})
        
        return {"message": "Directorio de animes", "data": lista_animes, "pagination": [{"prev_page": f"/api/anime/animeflv/directorio-animes?pagina={pagina - 1}" if pagina > 1 else None}, {"next_page": f"/api/anime/animeflv/directorio-animes?pagina={pagina + 1}"}], "code": 200}

    # Endpoint para buscar un anime en específico por su nombre
    def buscar_anime(self, anime_a_buscar: str = Query(..., description="Nombre del anime que quieres buscar.", example="shokugeki no souma")):
        
        # Hacemos cambios necesarios para la búsqueda
        soup = obtener_contenido_url(f"https://www3.animeflv.net/browse?q={anime_a_buscar.replace(' ', '+')}")
        
        # Buscamos los animes encontrados y los guardamos en una lista
        animes_encontrados = []
        for anime in soup.find("ul", {"class": "ListAnimes"}).find_all("li"):
            titulo = anime.find("h3").text
            image_src = anime.find("img")["src"]
            sinopsis = anime.find_all("p")[1].text
            anime_type = anime.find("span", {"class": "Type"}).text
            url_api = anime.find("a")["href"].replace("/anime/", "/api/anime/animeflv/info-anime?anime_a_buscar=")
            rating = anime.find("span", {"class": "Vts fa-star"}).text
            animeflv_info = f'https://www3.animeflv.net{anime.find_all("a")[1]["href"]}'

            # Agregamos los datos a la lista
            animes_encontrados.append({"title": titulo, "image_src": image_src, "sinopsis": sinopsis, "type": anime_type, "score": rating, "animeflv_info": animeflv_info, "url_api": url_api})
        
        return {"message": "Endpoint para buscar un anime en específico por su nombre", "data": animes_encontrados, "code": 200}

    # Endpoint para ver la info de un anime en específico
    def ver_info_anime(self, anime_a_buscar: str = Query(..., description="Nombre del anime que quieres ver su información.", example="sword art online")):
        
        # Hacemos cambios necesarios para la búsqueda
        anime_a_buscar = anime_a_buscar.replace(" ", "-").lower().replace(",", "").replace(":", "").replace("!", "").replace("(", "").replace(")", "").replace("?", "").replace("¿", "").replace("¡", "").replace("@", "")
        
        # Entramos a la página donde scrapearemos la información
        url = f"https://www3.animeflv.net/anime/{anime_a_buscar}"
        # Realiza una solicitud HTTP GET a la URL
        response = requests.get(url)
        
        # Si el anime se encuentra, se mostrará la información y si no, se mostrará un mensaje de error
        if response.status_code == 200:
            # Parsea el contenido HTML de la página
            soup = BeautifulSoup(response.content, "lxml")
            
            # Buscamos la información del anime
            titulo = soup.find("h1", {"class": "Title"}).text
            rating = soup.find("span", {"class": "vtprmd"}).text
            sinopsis = soup.find("div", {"class": "Description"}).find("p").text
            image = f'https://www3.animeflv.net{soup.find("div", {"class": "Image"}).find("img")["src"]}'
            tipo_anime = soup.find("span", {"class": "Type"}).text
            animeflv_info = f'https://www3.animeflv.net/anime/{anime_a_buscar}'
            
            # Ahora obtendremos los generos del anime
            generos = []
            for genero in soup.find("nav", {"class": "Nvgnrs"}).find_all("a"):
                generos.append(genero.text)
            
            # Obtendremos los nombres alternativos del anime
            nombres_alternativos = []
            try:
                html_nombres_alternativos = soup.find("span", {"class": "TxtAlt"})
                for nombre in html_nombres_alternativos:
                    nombres_alternativos.append(nombre.strip() if nombre else None)
            except:
                nombres_alternativos = []
                
            # Ahora obtendremos la lista de relacionados del anime
            relacionados = []
            html_relacionados = soup.find("ul", {"class": "ListAnmRel"})
            try:
                for relacionado in html_relacionados.find_all("li"):
                    titulo_relacionado = relacionado.find("a").text
                    tipo = relacionado.text.split("(")[1].replace(")", "").strip()
                    url_relacionado = relacionado.find("a")["href"].replace("/anime/", "/api/anime/animeflv/buscar-anime?anime_a_buscar=")
                    animeflv_info_relacionado = f'https://www3.animeflv.net{relacionado.find("a")["href"]}'
                    relacionados.append({"title": titulo_relacionado, "type": tipo, "animeflv_info": animeflv_info_relacionado, "url_api": url_relacionado})
            except:
                relacionados = []
            
            return {"message": "Endpoint para ver la info de un anime en específico", 
                    "data": {"title": titulo, "image_src": image, "alternative_names": nombres_alternativos, "sinopsis": sinopsis, "type": tipo_anime, "genres": generos, "relations": relacionados, "animeflv_info": animeflv_info, "score": rating}, "code": 200}
        else:
            return {"message": "Anime no encontrado.", "type": "Validation error.", "code": 422}
