# Importamos el router de la API
from fastapi import APIRouter
from animes.animeflv.animeflv_api import AnimeflvAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
animeflv_api = AnimeflvAPI()

router.add_api_route(
    path="/", endpoint=animeflv_api.hola_mundo, methods=["GET"], description="API de animeflv", name="Animeflv"
)
