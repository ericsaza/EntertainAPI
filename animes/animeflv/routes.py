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

# Endpoint para obtener el directorio de animes
router.add_api_route(
    path="/directorio-animes",
    endpoint=animeflv_api.ver_directorio_animes,
    methods=["GET"],
    description="Ver el directorio de animes en AnimeFLV.",
    name="Directorio de animes",
)

# Endpoint para buscar un anime por su nombre
router.add_api_route(
    path="/buscar-anime",
    endpoint=animeflv_api.buscar_anime,
    methods=["GET"],
    description="Buscar un anime por su nombre en AnimeFLV.",
    name="Buscar anime",
)