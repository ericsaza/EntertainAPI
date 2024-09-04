from enum import Enum
from fastapi import Query
from utils.scrap_utils import *


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
                "top_animes": "/api/anime/myanimelist/top-animes?page=1&top=all",
                "seasonal_animes": "/api/anime/myanimelist/seasonal-animes?year=2024&season=spring&anime_type=new",
                "search_anime": "/api/anime/myanimelist/search-anime?anime_name=Blue lock&page=1",
                "anime_info": "/api/anime/myanimelist/anime-info?myanimelist_id=21&anime_name=One Piece",
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
        for anime in guardar_varios_elementos_por_tag_y_atributo(
            soup, "tr", "class", "ranking-list"
        ):
            position = (
                guardar_elemento_por_tag_y_atributo(anime, "td", "class", "rank")
                .find("span")
                .text
            )
            myanimelist_id = (
                guardar_elemento_por_tag_y_atributo(
                    anime, "h3", "class", "fl-l fs14 fw-b anime_ranking_h3"
                )
                .find("a")["href"]
                .split("/")[4]
            )

            # Controlamos si no hay titulo
            title = (
                guardar_elemento_por_tag_y_atributo(
                    anime, "h3", "class", "fl-l fs14 fw-b anime_ranking_h3"
                )
                .find("a")
                .text
            )

            image_src = obtener_atributo_elemento_buscado_por_tag(
                anime, "img", "data-src"
            )

            start_date = f'{guardar_elemento_por_tag_y_atributo(anime, "div", "class", "information").get_text(strip=True, separator=" ").split(" ")[3]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[4]}'

            # Controlamos si no hay fecha de finalización
            try:
                end_date = f'{guardar_elemento_por_tag_y_atributo(anime, "div", "class", "information").get_text(strip=True, separator=" ").split(" ")[6]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[7]}'
            except Exception as e:
                end_date = None

            # Obtenemos el tipo de anime
            type = (
                guardar_varios_elementos_por_tag_y_atributo(
                    anime, "div", "class", "information"
                )[0]
                .get_text(strip=True, separator=" ")
                .split(" ")[0]
            )

            # Obtenemos la url de MyAnimeList
            url_myanimelist = guardar_elemento_por_tag_y_atributo(
                anime, "h3", "class", "fl-l fs14 fw-b anime_ranking_h3"
            ).find("a")["href"]

            score = (
                guardar_elemento_por_tag_y_atributo(anime, "td", "class", "score")
                .find("span")
                .text
            )
            url_api = f"/api/anime/myanimelist/anime-info?myanimelist_id={myanimelist_id}&anime_name={title}"

            # Agregamos los datos a la lista
            lista_animes.append(
                {
                    "position": position,
                    "mal_id": myanimelist_id,
                    "title": title,
                    "image_src": image_src,
                    "dates": {
                        "start_date": start_date,
                        "end_date": (None if "members" in end_date else end_date),
                    },  # Controlo que si lo que recibe no es una fecha de null
                    "type": type,
                    "score": score,
                    "url_mal": url_myanimelist,
                    "url_api": url_api,
                }
            )

        # Devolvemos la información
        return {
            "message": "Emdpoint to see top 50 animes on MyAnimeList.",
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
        new = guardar_varios_elementos_por_tag_y_atributo(
            soup, "div", "class", "seasonal-anime-list"
        )[index]
        animes = []
        for anime in guardar_varios_elementos_por_tag_y_atributo(
            new, "div", "class", "seasonal-anime"
        ):
            myanimelist_id = (
                guardar_elemento_por_tag_y_atributo(
                    anime, "h2", "class", "h2_anime_title"
                )
                .find("a")["href"]
                .split("/")[4]
            )

            # Obtenemos la información de los animes
            title = (
                guardar_elemento_por_tag_y_atributo(
                    anime, "h2", "class", "h2_anime_title"
                )
                .find("a")
                .text.replace('"', '')
            )
            image_src = (
                guardar_elemento_por_tag_y_atributo(anime, "div", "class", "image")
                .find("img")
                .get("src")
            )
            myanimelist_url = guardar_elemento_por_tag_y_atributo(
                anime, "h2", "class", "h2_anime_title"
            ).find("a")["href"]

            # Controlamos si no hay score
            try:
                score = float(
                    obtener_texto_elemento_buscado_por_tag_y_atributo(
                        anime, "div", "class", "score"
                    )
                )
            except Exception as e:
                score = None
            sinopsis = obtener_texto_elemento_buscado_por_tag_y_atributo(
                anime, "p", "class", "preline"
            )
            studio = (
                guardar_elemento_por_tag_y_atributo(anime, "div", "class", "property")
                .find("span", {"class", "item"})
                .text
            )
            source = (
                guardar_varios_elementos_por_tag_y_atributo(
                    anime, "div", "class", "property"
                )[1]
                .find("span", {"class", "item"})
                .text
            )

            # Añadimos los géneros
            genres = []
            for genre in guardar_varios_elementos_por_tag_y_atributo(
                anime, "span", "class", "genre"
            ):
                genres.append(genre.get_text(strip=True))

            animes.append(
                {
                    "mal_id": myanimelist_id,
                    "title": title,
                    "image_src": image_src,
                    "genres": genres,
                    "studio": studio,
                    "source": source,
                    "sinopsis": sinopsis,
                    "score": score,
                    "url_mal": myanimelist_url,
                    "url_api": f"/api/anime/myanimelist/anime-info?myanimelist_id={myanimelist_id}&anime_name={title}",
                }
            )

        return {
            "message": f"Endpoint to see {anime_type.value} animes of {season.value} {year}",
            "data": animes,
            "code": 200,
        }

    # Endpoint para buscar un anime por su nombre
    def buscar_anime(
        self,
        anime_name: str = Query(
            ...,
            example="Blue lock",
            description="Name of the anime you want to search.",
        ),
        page: int = Query(
            ..., example=1, description="Number of the page you want to see."
        ),
    ):
        # Entramos a la página donde scrapearemos la información
        soup = obtener_contenido_url(
            f"https://myanimelist.net/anime.php?cat=anime&q={anime_name}&show={50 * (page - 1)}&ey=0&c%5B%5D=a&c%5B%5D=b&c%5B%5D=c&c%5B%5D=d&c%5B%5D=e&c%5B%5D=g"
        )

        lista_animes = []
        # Recorreremos todos los 'tr' menos el primero que es el header
        for anime in guardar_elemento_por_tag_y_atributo(
            soup, "div", "class", "js-categories-seasonal js-block-list list"
        ).find_all("tr")[1:]:
            myanimelist_id = obtener_atributo_elemento_buscado_por_tag(
                anime, "a", "href"
            ).split("/")[4]
            title = obtener_texto_elemento_buscado_por_tag(anime, "strong")
            image_src = obtener_atributo_elemento_buscado_por_tag(
                anime, "img", "data-src"
            )
            sinopsis = obtener_texto_elemento_buscado_por_tag_y_atributo(
                anime, "div", "class", "pt4"
            ).replace("read more.", "")
            type = guardar_varios_elementos_por_tag(anime, "td")[2].get_text(strip=True)
            try:
                rating = float(
                    guardar_varios_elementos_por_tag(anime, "td")[4].get_text(
                        strip=True
                    )
                )
            except Exception as e:
                rating = None
            start_date = guardar_varios_elementos_por_tag(anime, "td")[5].get_text(
                strip=True
            )
            end_date = guardar_varios_elementos_por_tag(anime, "td")[6].get_text(
                strip=True
            )
            myanimelist_url = obtener_atributo_elemento_buscado_por_tag(
                anime, "a", "href"
            )

            lista_animes.append(
                {
                    "mal_id": myanimelist_id,
                    "title": title,
                    "image_src": image_src,
                    "type": type,
                    "sinopsis": sinopsis,
                    "dates": {
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                    "score": rating,
                    "url_mal": myanimelist_url,
                    "url_api": f"/api/anime/myanimelist/anime-info?myanimelist_id={myanimelist_id}&anime_name={title}",
                }
            )

        return {
            "message": f"Endpoints to search anime by name",
            "data": lista_animes,
            "pagination": {
                "prev_page": (
                    f"/api/anime/myanimelist/search-anime?anime_name={anime_name}&page={page - 1}"
                    if page > 1
                    else None
                ),
                "next_page": f"/api/anime/myanimelist/search-anime?anime_name={anime_name}&page={page + 1}",
            },
            "code": 200,
        }

    # Endpoint para ver la información de un anime
    def informacion_anime(
        self,
        myanimelist_id: int = Query(
            ..., example=21, description="MyAnimeList ID of the anime."
        ),
        anime_name: str = Query("One Piece", description="Name of the anime."),
    ):
        # Entramos a la página donde scrapearemos la información
        soup = obtener_contenido_url(
            f"https://myanimelist.net/anime/{myanimelist_id}/{anime_name.replace(' ', '_').replace(':', '').replace('!', '').replace('?', '')}"
        )

        # Obtenemos la información del anime
        # Controlamos si no hay rank
        try:
            rank = int(
                guardar_elemento_por_tag_y_atributo(
                    soup, "span", "class", "numbers ranked"
                )
                .find("strong")
                .get_text(strip=True)
                .replace("#", "")
            )
        except Exception as e:
            rank = None

        # Controlamos si no hay popularity rank
        try:
            popularity_rank = int(
                guardar_elemento_por_tag_y_atributo(
                    soup, "span", "class", "numbers popularity"
                )
                .find("strong")
                .get_text(strip=True)
                .replace("#", "")
            )
        except Exception as e:
            popularity_rank = None

        title = obtener_texto_elemento_buscado_por_tag_y_atributo(
            soup, "h1", "class", "title-name"
        )
        image_src = guardar_elemento_por_tag_y_atributo(
            soup, "div", "class", "leftside"
        ).find("img")["data-src"]
        sinopsis = obtener_texto_elemento_buscado_por_tag_y_atributo(
            soup, "p", "itemprop", "description"
        )
        video_promo = guardar_elemento_por_tag_y_atributo(
            soup, "div", "class", "video-promotion"
        ).find("a")["href"]
        type = (
            guardar_elemento_por_texto(soup, "h2", "Information")
            .find_next("div")
            .find("a")
            .text
        )

        # Controlamos si no hay episodios
        try:
            episodes = int(
                guardar_elemento_por_texto(soup, "span", "Episodes:")
                .find_parent()
                .get_text(strip=True)
                .split(":")[1]
            )
        except Exception as e:
            episodes = None

        studio = (
            guardar_elemento_por_texto(soup, "span", "Studios:")
            .find_parent()
            .get_text(strip=True)
            .split(":")[1]
        )
        source = (
            guardar_elemento_por_texto(soup, "span", "Source:")
            .find_parent()
            .get_text(strip=True)
            .split(":")[1]
        )

        # Controlamos si no hay score
        try:
            score = float(
                obtener_texto_elemento_buscado_por_tag_y_atributo(
                    soup, "div", "class", "score-label"
                )
            )
        except Exception as e:
            score = None

        # Dependiendo del anime puede tener un solo genero o varios asi que controlamos si es uno o varios
        try:
            genres = (
                guardar_elemento_por_texto(soup, "span", "Genre:")
                .find_parent()
                .get_text(strip=True, separator=" ")
                .split(":")[1]
                .split(" ")[1]
            )
        except Exception as e:
            genres = (
                guardar_elemento_por_texto(soup, "span", "Genres:")
                .find_parent()
                .get_text(strip=True, separator=" ")
                .split(":")[1]
                .split(",")
            )

            # Recorremos los generos y eliminamos los espacios
            for i in range(len(genres)):
                genres[i] = genres[i].split(" ")[1]

        # Controlamos si no hay tema
        try:
            theme = (
                guardar_elemento_por_texto(soup, "span", "Theme:")
                .find_parent()
                .get_text(strip=True, separator="-")
                .split(":")[1]
                .split("-")[1]
            )

        except Exception as e:
            theme = None

        # Controlamos si no hay demografico
        try:
            demographic = (
                guardar_elemento_por_texto(soup, "span", "Demographic:")
                .find_parent()
                .get_text(strip=True, separator=" ")
                .split(":")[1]
                .split(" ")[1]
            )
        except Exception as e:
            demographic = None

        # Obtendremos los personajes principales y sus actores de voz
        characters = []
        for character in range(10):
            try:
                character_name = (
                    guardar_varios_elementos_por_tag_y_atributo(
                        soup, "h3", "class", "h3_characters_voice_actors"
                    )[len(characters)]
                    .find("a")
                    .text
                )
                voice_actor = (
                    guardar_varios_elementos_por_tag_y_atributo(
                        soup, "td", "class", "va-t ar pl4 pr4"
                    )[len(characters)]
                    .find("a")
                    .text
                )

                # Agregamos los datos a la lista
                characters.append(
                    {
                        "character_name": character_name,
                        "voice_actor": voice_actor,
                    }
                )
            except Exception as e:
                break

        # Añadimos al staff
        staff = []
        for staff_member in guardar_varios_elementos_por_tag_y_atributo(soup, "div", "class", "detail-characters-list clearfix")[1].find_all("table"):
            staff_name = guardar_varios_elementos_por_tag(staff_member, "a")[1].text
            staff_role = obtener_texto_elemento_buscado_por_tag(staff_member, "small")
            staff.append({"staff_name": staff_name, "staff_role": staff_role})

        return {
            "message": f"Endpoint to see information about an anime",
            "data": {
                "rank_position": rank,
                "popularity_rank_position": popularity_rank,
                "title": title,
                "image_src": image_src,
                "num_episodes": episodes,
                "video_promotion": video_promo,
                "type": type,
                "studio": studio,
                "source": source,
                "genres": genres,
                "theme": theme,
                "demographic": demographic,
                "sinopsis": sinopsis,
                "characters": characters,
                "staff": staff,
                "score": score,
            },
            "code": 200,
        }
