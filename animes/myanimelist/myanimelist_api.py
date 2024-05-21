from enum import Enum
from fastapi import Query
from utils.scrap_utils import obtener_contenido_url


# Enum de tipos de tops
class TopTypes(str, Enum):
    top_all = "all"
    top_airing = "airing"
    top_tv = "tv"
    top_ova = "ova"
    top_popular = "bypopularity"
    top_favorite = "favorite"
    top_movies = "movie"


# Enum de tipos de temporadas
class SeasonTypes(str, Enum):
    winter = "winter"
    spring = "spring"
    summer = "summer"
    fall = "fall"


# Enum tipo de animes
class SeasonalAnimeTypes(str, Enum):
    new = "new"
    continuing = "continuing"
    onas = "onas"
    ovas = "ovas"
    movies = "movies"
    specials = "specials"


class MyAnimeListAPI:

    # Endpoint para ver la información de la API de MyAnimeList
    def info_endpoint(self):
        return {
            "message": "Endpoint to view MyAnimeList API information.",
            "description": "This endpoint will show you MyAnimeList API information, including available endpoints, API documentation, and response code.",
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
        page: int = Query(
            ..., example=1, description="Number of the page you want to see."
        ),
        top: TopTypes = Query(
            ..., example=TopTypes.top_all, description="Type of top anime."
        ),
    ):
        # Entramos a la página donde scrapearemos la información
        soup = obtener_contenido_url(
            f"https://myanimelist.net/topanime.php?type={top.value}&limit={50 * (page - 1)}"
        )

        # Buscamos la información de los animes
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
                        f"/api/anime/myanimelist/top-animes?pagina={page - 1}"
                        if page > 1
                        else None
                    )
                },
                {"next_page": f"/api/anime/myanimelist/top-animes?pagina={page + 1}"},
            ],
            "code": 200,
        }

    def seasonal_animes(
        self,
        year: int = Query(..., example=2024, description="Year of the season."),
        season: SeasonTypes = Query(
            ..., example=SeasonTypes.spring, description="Season of the year."
        ),
        anime_type: SeasonalAnimeTypes = Query(
            ..., example=SeasonalAnimeTypes.new, description="Type of anime."
        ),
    ):
        # Entramos a la página donde scrapearemos la información
        soup = obtener_contenido_url(
            f"https://myanimelist.net/anime/season/{year}/{season.value}"
        )
        index = 0
        if anime_type.value == "new":
            index = 0
        elif anime_type.value == "continuing":
            index = 1
        elif anime_type.value == "onas":
            index = 2
        elif anime_type.value == "ovas":
            index = 3
        elif anime_type.value == "movies":
            index = 4
        elif anime_type.value == "specials":
            index = 5

        # Obtenemos la información de los animes de temporada
        # empeza por new
        new = soup.find_all("div", {"class": "seasonal-anime-list"})[index]
        animes = []
        for anime in new.find_all("div", {"class": "seasonal-anime"}):
            myanimelist_id = anime.find("h2", {"class": "h2_anime_title"}).find("a")["href"].split("/")[4]
            title = anime.find("h2", {"class": "h2_anime_title"}).find("a").text
            image_src = anime.find("div", {"class": "image"}).find("img").get('src')
            myanimelist_url = anime.find("h2", {"class": "h2_anime_title"}).find("a")["href"]
            score = anime.find("div", {"class": "score"}).get_text(strip=True)
            sinposis = anime.find("p", {"class": "preline"}).get_text(strip=True)
            studio = anime.find_all("div", {"class": "property"})[0].find("span", {"class", "item"}).text
            source = anime.find_all("div", {"class": "property"})[1].find("span", {"class", "item"}).text
            
            # Añadimos los géneros
            genres = []
            for genre in anime.find_all("span", {"class": "genre"}):
                genres.append(genre.get_text(strip=True))

            animes.append({"mal_id": myanimelist_id, "title": title, "image_src": image_src, "sinopsis": sinposis, "genres": genres, "studio": studio, "source": source, "url_mal": myanimelist_url, "score": score})

        return {
            "message": f"Animes of the season {season.value} of {year}",
            "data": animes,
            "code": 200,
        }
