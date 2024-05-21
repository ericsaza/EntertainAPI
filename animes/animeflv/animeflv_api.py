from bs4 import BeautifulSoup
import requests
from scrapper.utils import obtener_contenido_url


class AnimeflvAPI:
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