# Importamos el router de la API
from fastapi import APIRouter
from principal.api import PrincipalAPI

# Instanciamos un router
router = APIRouter()

# Instanciamos la clase PrincipalAPI
api = PrincipalAPI()

router.add_api_route(path="/", endpoint=api.hola_mundo, methods=["GET"]) # Con el "include_in_schema=False" ocultamos la ruta de la documentación de la API (Swagger y ReDoc
