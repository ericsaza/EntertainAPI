# Importamos el router de la API
from fastapi import APIRouter
from animes.animeflv.animeflv_api import AnimeflvAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
animeflv_api = AnimeflvAPI()

# Endpoint para obtener los últimos episodios de animes
router.add_api_route(
    path="/episodios-recientes",
    endpoint=animeflv_api.episodios_recientes,
    methods=["GET"],
    description="Ver los útimos episodios agregados en AnimeFLV.",
    name="Episodios recientes",
)

# Endpoint para obtener los últimos animes añadidos
router.add_api_route(
    path="/ultimos-animes",
    endpoint=animeflv_api.mostrar_ultimos_animes,
    methods=["GET"],
    description="Ver los últimos animes añadidos en AnimeFLV.",
    name="Últimos animes",
)