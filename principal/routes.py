# Importamos el router de la API
from fastapi import APIRouter
from principal.api import PrincipalAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
api = PrincipalAPI()

router.add_api_route(
    path="/", endpoint=api.hola_mundo, methods=["GET"]
)
