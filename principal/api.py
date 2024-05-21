# Creamos la clase principal de la API
class PrincipalAPI:

    # Método para la ruta principal de la API
    def hola_mundo(
        self,
    ):  # el "self" es necesario para que FastAPI pueda reconocer el método
        return {
            "message": "API de entretenimiento - EntertainAPI",
            "description": "EntertainAPI es una interfaz de programación de aplicaciones (API) diseñada para ofrecer acceso fácil y rápido a una amplia variedad de datos relacionados con entretenimiento, incluyendo información sobre películas, series, animes, mangas y más.",
            "endpoints": {},
            "documentation": {"swagger": "/docs", "doc": "/redoc"},
            "code": 200,
        }
