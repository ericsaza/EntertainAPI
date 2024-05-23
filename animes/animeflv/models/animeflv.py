from typing import List
from pydantic import BaseModel

# Clase que representa un episodio
class Episodio(BaseModel):
    title: str
    episode: int
    image_src: str
    url: str

# Clase que representa uno de los últimos animes añadidos
class AnimeAnadido(BaseModel):
    title: str
    image_src: str
    sinopsis: str
    type: str
    score: float
    animeflv_info: str
    url_api: str
    
# Clase que representa un anime del directorio de animes
class AnimeDirectorio(BaseModel):
    title: str
    image_src: str
    sinopsis: str
    type: str
    score: float
    animeflv_info: str
    url_api: str

# Clase que representa una relación de un anime
class AnimeRelacion(BaseModel):
    title: str
    type: str
    animeflv_info: str
    url_api: str

# Clase que representa un anime buscado
class AnimeBuscado(BaseModel):
    title: str
    image_src: str
    alternative_names: List[str]
    sinopsis: str
    type: str
    genres: List[str]
    relations: List[AnimeRelacion]
    animeflv_info: str
    score: float
    
# Clase que representa la paginación
class Pagination(BaseModel):
    prev_page: str | None
    next_page: str | None
    
# Clase que representa la respuesta de los episodios recientes
class EpisodiosRecientesResponse(BaseModel):
    message: str
    data: List[Episodio] 
    code: int = 200

# Clase que representa la respuesta de los últimos animes añadidos
class UltimosAnimesResponse(BaseModel):
    message: str
    data: List[AnimeAnadido]
    code: int = 200

# Clase que representa la respuesta del directorio de animes
class DirectorioAnimesResponse(BaseModel):
    message: str
    data: List[AnimeDirectorio]
    pagination: Pagination
    code: int = 200

# Clase que representa la respuesta de la búsqueda de un anime
class BuscadorAnimeResponse(BaseModel):
    message: str
    data: List[AnimeDirectorio]
    code: int = 200

# Clase que representa la respuesta de la información de un anime
class VerInfoAnimeAnimeResponse(BaseModel):
    message: str
    data: AnimeBuscado
    code: int = 200