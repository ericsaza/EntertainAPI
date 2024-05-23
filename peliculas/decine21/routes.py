# Importamos el router de la API
from fastapi import APIRouter
from peliculas.decine21.decine21_api import Decine21API
from peliculas.decine21.models.decine21 import CalendarioEstrenosResponse


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

# Endpoint para ver el calendario de estrenos de Decine21
router.add_api_route(
    path="/calendario-estrenos",
    endpoint=decine21_api.calendario_estrenos,
    methods=["GET"],
    description="Ver el calendario de estrenos de Decine21.",
    name="Calendario de Estrenos",
    response_model=CalendarioEstrenosResponse,
)