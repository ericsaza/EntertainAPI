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
                "top_animes": "/api/anime/myanimelist/top-animes?page=1&top=all"
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

            start_date = f'{anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[3]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[4]}'
            end_date = f'{anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[6]} {anime.find("div", {"class": "information"}).get_text(strip=True, separator=" ").split(" ")[7]}'
            type = (
                anime.find("div", {"class": "information"})
                .get_text(strip=True, separator=" ")
                .split(" ")[0]
            )
            url_myanimelist = anime.find(
                "h3", {"class": "fl-l fs14 fw-b anime_ranking_h3"}
            ).find("a")["href"]
            score = anime.find("td", {"class": "score"}).find("span").text
            url_api = f"/api/anime/myanimelist/anime-info?myanimelist_id={myanimelist_id}&anime_name={title}"

            # Agregamos los datos a la lista
            lista_animes.append(
                {
                    "position": int(position),
                    "mal_id": int(myanimelist_id),
                    "title": title,
                    "image_src": image_src,
                    "dates": {
                        "start_date": start_date,
                        "end_date": (None if "members" in end_date else end_date),
                    },  # Controlo que si lo que recibe no es una fecha de null
                    "type": type,
                    "score": float(score),
                    "url_mal": url_myanimelist,
                    "url_api": url_api,
                }
            )

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
        new = soup.find_all("div", {"class": "seasonal-anime-list"})[index]
        animes = []
        for anime in new.find_all("div", {"class": "seasonal-anime"}):
            myanimelist_id = (
                anime.find("h2", {"class": "h2_anime_title"})
                .find("a")["href"]
                .split("/")[4]
            )
            title = anime.find("h2", {"class": "h2_anime_title"}).find("a").text
            image_src = anime.find("div", {"class": "image"}).find("img").get("src")
            myanimelist_url = anime.find("h2", {"class": "h2_anime_title"}).find("a")[
                "href"
            ]

            # Controlamos si no hay score
            try:
                score = float(
                    anime.find("div", {"class": "score"}).get_text(strip=True)
                )
            except Exception as e:
                score = None
            synopsis = anime.find("p", {"class": "preline"}).get_text(strip=True)
            studio = (
                anime.find_all("div", {"class": "property"})[0]
                .find("span", {"class", "item"})
                .text
            )
            source = (
                anime.find_all("div", {"class": "property"})[1]
                .find("span", {"class", "item"})
                .text
            )

            # Añadimos los géneros
            genres = []
            for genre in anime.find_all("span", {"class": "genre"}):
                genres.append(genre.get_text(strip=True))

            animes.append(
                {
                    "mal_id": int(myanimelist_id),
                    "title": title,
                    "image_src": image_src,
                    "genres": genres,
                    "studio": studio,
                    "source": source,
                    "synopsis": synopsis,
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
        for anime in soup.find(
            "div", {"class": "js-categories-seasonal js-block-list list"}
        ).find_all("tr")[1:]:
            myanimelist_id = anime.find("a")["href"].split("/")[4]
            title = anime.find("strong").get_text(strip=True)
            image_src = anime.find("img")["data-src"]
            synopsis = (
                anime.find("div", {"class": "pt4"})
                .get_text(strip=True)
                .replace("read more.", "")
            )
            type = anime.find_all(
                "td",
            )[
                2
            ].get_text(strip=True)
            try:
                rating = float(
                    anime.find_all(
                        "td",
                    )[
                        4
                    ].get_text(strip=True)
                )
            except Exception as e:
                rating = None
            start_date = anime.find_all(
                "td",
            )[
                5
            ].get_text(strip=True)
            end_date = anime.find_all(
                "td",
            )[
                6
            ].get_text(strip=True)
            myanimelist_url = anime.find("a")["href"]

            lista_animes.append(
                {
                    "mal_id": myanimelist_id,
                    "title": title,
                    "image_src": image_src,
                    "type": type,
                    "synopsis": synopsis,
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
            "pagination": [
                {
                    "prev_page": (
                        f"/api/anime/myanimelist/search-anime?anime_name={anime_name}&page={page - 1}"
                        if page > 1
                        else None
                    )
                },
                {
                    "next_page": f"/api/anime/myanimelist/search-anime?anime_name={anime_name}&page={page + 1}"
                },
            ],
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
            soup.find("span", {"class": "numbers ranked"})
            .find("strong")
            .get_text(strip=True)
            .replace("#", "")
        )
        except Exception as e:
            rank = None
            
        
        # Controlamos si no hay popularity rank
        try:
            popularity_rank = int(
            soup.find("span", {"class": "numbers popularity"})
            .find("strong")
            .get_text(strip=True)
            .replace("#", "")
        )
        except Exception as e:
            popularity_rank = None
        
        
        title = soup.find("h1", {"class": "title-name"}).text
        image_src = soup.find("div", {"class": "leftside"}).find("img")["data-src"]
        synopsis = soup.find("p", {"itemprop": "description"}).text
        video_promo = soup.find("div", {"class": "video-promotion"}).find("a")["href"]
        type = soup.find("h2", string="Information").find_next("div").find("a").text
        
        # Controlamos si no hay episodios
        try:
            episodes = int(
            soup.find("span", string="Episodes:")
            .find_parent()
            .get_text(strip=True)
            .split(":")[1]
        )
        except Exception as e:
            episodes = None
            
        studio = (
            soup.find("span", string="Studios:")
            .find_parent()
            .get_text(strip=True)
            .split(":")[1]
        )
        source = (
            soup.find("span", string="Source:")
            .find_parent()
            .get_text(strip=True)
            .split(":")[1]
        )

        # Controlamos si no hay score
        try:
            score = float(soup.find("div", {"class": "score-label"}).text)
        except Exception as e:
            score = None
            
        # Dependiendo del anime puede tener un solo genero o varios asi que controlamos si es uno o varios
        try:
            genres = (
                soup.find("span", string="Genre:")
                .find_parent()
                .get_text(strip=True, separator=" ")
                .split(":")[1]
                .split(" ")[1]
            )
        except Exception as e:
            genres = (
                soup.find("span", string="Genres:")
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
                soup.find("span", string="Theme:")
                .find_parent()
                .get_text(strip=True, separator="-")
                .split(":")[1]
                .split("-")[1]
            )
        except Exception as e:
            theme = None
        demographic = (
            soup.find("span", string="Demographic:")
            .find_parent()
            .get_text(strip=True, separator=" ")
            .split(":")[1]
            .split(" ")[1]
        )

        # Obtendremos los personajes principales y sus actores de voz
        characters = []
        for character in range(10):
            try:
                character_name = (
                    soup.find_all("h3", {"class": "h3_characters_voice_actors"})[
                        character
                    ]
                    .find("a")
                    .text
                )
                voice_actor = (
                    soup.find_all("td", {"class": "va-t ar pl4 pr4"})[len(characters)]
                    .find("a")
                    .text
                )

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
        for staff_member in soup.find_all(
            "div", {"class": "detail-characters-list clearfix"}
        )[1].find_all("table"):
            staff_name = staff_member.find_all("a")[1].text
            staff_role = staff_member.find("small").text
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
                "synopsis": synopsis,
                "characters": characters,
                "staff": staff,
                "score": score,
            },
            "code": 200,
        }
