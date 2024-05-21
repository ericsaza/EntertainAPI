from bs4 import BeautifulSoup
import requests
from scrapper.utils import obtener_contenido_url


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