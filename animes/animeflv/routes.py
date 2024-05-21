# Importamos el router de la API
from fastapi import APIRouter
from animes.animeflv.animeflv_api import AnimeflvAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
animeflv_api = AnimeflvAPI()

router.add_api_route(
    path="/",
    endpoint=animeflv_api.episodios_recientes,
    methods=["GET"],
    description="Ver los útimos episodios agregados en AnimeFLV.",
    name="Episodios recientes",
)
