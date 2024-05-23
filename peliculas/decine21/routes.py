# Importamos el router de la API
from fastapi import APIRouter
from peliculas.decine21.decine21_api import Decine21API


# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
decine21_api = Decine21API()

# Endpoint para ver la información de la API
router.add_api_route(
    path="/",
    endpoint=decine21_api.info_endpoint,
    methods=["GET"],
    description="Ver la información de la API de Decine21.",
    name="Info",
    include_in_schema=False,
)