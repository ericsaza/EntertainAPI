from enum import Enum
from fastapi import Query
from scrapper.utils import obtener_contenido_url


class TopTypes(str, Enum):
    top_all = "all"
    top_airing = "airing"
    top_tv = "tv"
    top_ova = "ova"
    top_popular = "bypopularity"
    top_favorite = "favorite"
    top_movies = "movie"


class MyAnimeListAPI:

    # Endpoint para ver la información de la API de MyAnimeList
    def info_endpoint(self):
        return {
            "message": "Endpoint para ver la información de la API de MyAnimeList.",
            "description": "Este endpoint te mostrará la información de la API de MyAnimeList, incluyendo los endpoints disponibles, la documentación de la API y el código de respuesta.",
            "endpoints": {
                "top_animes": "/api/anime/myanimelist/top-animes?pagina=1&top=all"
            },
            "other_anime_endpoints": {
                "AnimeFLV": "/api/anime/animeflv",
            },
            "documentation": {"swagger": "/docs", "doc": "/redoc"},
            "code": 200,
        }

    # Endpoint para obtener el top de animes
    def top_animes(
        self,
        pagina: int = Query(
            ..., example=1, description="Número de la página que deseas ver."
        ),
        top: TopTypes = Query(
            ..., example=TopTypes.top_all, description="Que top deseas ver."
        ),
    ):
        # Entramos a la página donde scrapearemos la información
        soup = obtener_contenido_url(
            f"https://myanimelist.net/topanime.php?type={top.value}&limit={50 * (pagina - 1)}"
        )

        # Buscamos todos los animes
        lista_animes = []
        for anime in soup.find_all("tr", {"class": "ranking-list"}):
            position = anime.find("td", {"class": "rank"}).find("span").text
            myanimelist_id = (
                anime.find("h3", {"class": "fl-l fs14 fw-b anime_ranking_h3"})
                .find("a")["href"]
                .split("/")[4]
            )
            title = (
                anime.find("h3", {"class": "fl-l fs14 fw-b anime_ranking_h3"})
                .find("a")
                .text
            )
            image_src = anime.find("img")["data-src"]
            num_episodes = (
                anime.find("div", {"class": "information"})
                .get_text(strip=True, separator=" ")
                .split(" ")[1]
                .replace("(", "")
            )
            airing_date = f'{anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[3]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[4]}'
            finalization_date = f'{anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[6]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[7]}'
            type = (
                anime.find("div", {"class": "information"})
                .get_text(strip=True, separator=" ")
                .split(" ")[0]
            )
            url_myanimelist = anime.find(
                "h3", {"class": "fl-l fs14 fw-b anime_ranking_h3"}
            ).find("a")["href"]
            score = anime.find("td", {"class": "score"}).find("span").text

            # Agregamos los datos a la lista
            lista_animes.append(
                {
                    "position": position,
                    "mal_id": myanimelist_id,
                    "title": title,
                    "image_src": image_src,
                    "num_episodes": num_episodes,
                    "dates": {
                        "airing_date": airing_date,
                        "finalization_date": (
                            None
                            if "members" in finalization_date
                            else finalization_date
                        ),
                    },  # Controlo que si lo que recibe no es una fecha de null
                    "type": type,
                    "url_mal": url_myanimelist,
                    "score": score,
                }
            )

        return {
            "message": "Top 50 animes",
            "data": lista_animes,
            "pagination": [
                {
                    "prev_page": (
                        f"/api/anime/myanimelist/top-animes?pagina={pagina - 1}"
                        if pagina > 1
                        else None
                    )
                },
                {"next_page": f"/api/anime/myanimelist/top-animes?pagina={pagina + 1}"},
            ],
            "code": 200,
        }
