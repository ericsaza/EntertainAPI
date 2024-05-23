# Creamos la clase principal de la API
class PrincipalAPI:

    # Método para la ruta principal de la API
    def hola_mundo(
        self,
    ):  # el "self" es necesario para que FastAPI pueda reconocer el método
        return {
            "message": "API de entretenimiento - EntertainAPI",
            "description": "EntertainAPI es una interfaz de programación de aplicaciones (API) diseñada para ofrecer acceso fácil y rápido a una amplia variedad de datos relacionados con entretenimiento, incluyendo información sobre películas, series, animes, mangas y más.",
            "endpoints": {
                "animes": {
                    "AnimeFLV": {
                        "episodios_recientes": "/api/anime/animeflv/episodios-recientes",
                        "ultimos_animes": "/api/anime/animeflv/ultimos-animes",
                        "directorio_animes": "/api/anime/animeflv/directorio-animes?pagina=1",
                        "buscar_anime": "/api/anime/animeflv/buscar-anime?anime_a_buscar=sword%20art%20online",
                        "ver_info_anime": "/api/anime/animeflv/info-anime?anime_a_buscar=sword%20art%20online",
                    },
                    "endpoints": {
                        "top_animes": "/api/anime/myanimelist/top-animes?page=1&top=all",
                        "seasonal_animes": "/api/anime/myanimelist/seasonal-animes?year=2024&season=spring&type=new",
                        "search_anime": "/api/anime/myanimelist/search-anime?anime_name=Blue lock&page=1",
                        "anime_info": "/api/anime/myanimelist/anime-info?myanimelist_id=21&anime_name=One Piece",
                    },
                },
                "mangas": {},
                "peliculas": {},
            },
            "documentation": {"swagger": "/docs", "doc": "/redoc"},
            "code": 200,
        }
