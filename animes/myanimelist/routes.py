# Importamos el router de la API
from fastapi import APIRouter
from animes.myanimelist.myanimelist_api import MyAnimeListAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
myanimelist_api = MyAnimeListAPI()

# Endpoint para ver la información de la API
router.add_api_route(
    path="/",
    endpoint=myanimelist_api.info_endpoint,
    methods=["GET"],
    description="Ver la información de la API de MyAnimeList.",
    name="Info",
    include_in_schema=False,
)

# Endpoint para obtener el top de animes
router.add_api_route(
    path="/top-animes",
    endpoint=myanimelist_api.top_animes,
    methods=["GET"],
    description="Ver el top de animes en MyAnimeList.",
    name="Top animes",
)