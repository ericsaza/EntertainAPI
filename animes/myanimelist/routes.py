# Importamos el router de la API
from fastapi import APIRouter
from animes.myanimelist.myanimelist_api import MyAnimeListAPI
from animes.myanimelist.models.myanimelist import AnimeTopResponse, SeasonalAnimesResponse, BuscadorAnimeResponse

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
myanimelist_api = MyAnimeListAPI()

# Endpoint para ver la información de la API
router.add_api_route(
    path="/",
    endpoint=myanimelist_api.info_endpoint,
    methods=["GET"],
    description="View MyAnimeList API information.",
    name="Info",
    include_in_schema=False,
)

# Endpoint para obtener el top de animes
router.add_api_route(
    path="/top-animes",
    endpoint=myanimelist_api.top_animes,
    methods=["GET"],
    description="See the top animes on MyAnimeList.",
    name="Top animes",
    response_model=AnimeTopResponse
)

# Endpoint para ver los animes de temporada
router.add_api_route(
    path="/seasonal-animes",
    endpoint=myanimelist_api.seasonal_animes,
    methods=["GET"],
    description="See seasonal anime on MyAnimeList.",
    name="Animes de temporada",
    response_model=SeasonalAnimesResponse,
)

# Endpoint para buscar un anime por su nombre
router.add_api_route(
    path="/search-anime",
    endpoint=myanimelist_api.buscar_anime,
    methods=["GET"],
    description="Search an anime by its name on MyAnimeList.",
    name="Search anime",
    response_model=BuscadorAnimeResponse,
)

# Endpoint para ver la información de un anime
router.add_api_route(
    path="/anime-info",
    endpoint=myanimelist_api.informacion_anime,
    methods=["GET"],
    description="View information about an anime on MyAnimeList.",
    name="Anime info",
)