from typing import List
from pydantic import BaseModel

# Clase que representa las fechas de inicio y fin de un anime del top de MyAnimeList
class Dates(BaseModel):
    start_date: str
    end_date: str | None

# Clase que representa un anime del top de MyAnimeList
class AnimeTop(BaseModel):
    position: int
    mal_id: int
    title: str
    image_src: str
    dates: Dates
    type: str
    score: float
    url_mal: str
    url_api: str
    
# Clase que representa un anime de temporada de MyAnimeList
class SeasonalAnime(BaseModel):
    mal_id: int
    title: str
    image_src: str | None
    genres: List[str]
    studio: str
    source: str
    sinopsis: str
    score: float | None
    url_mal: str
    url_api: str
    
# Clase que representa un anime buscado en MyAnimeList
class BuscadorAnime(BaseModel):
    mal_id: int
    title: str
    image_src: str
    type: str
    sinopsis: str
    dates: Dates
    score: float | None
    url_mal: str
    url_api: str
    
class Character(BaseModel):
    character_name: str
    voice_actor: str

class Staff(BaseModel):
    staff_name: str
    staff_role: str

# Clase que representa la información de un anime en MyAnimeList
class AnimeInfo(BaseModel):
    rank_position: int | None
    popularity_rank_position: int | None
    title: str
    image_src: str
    num_episodes: int | None
    video_promotion: str | None
    type: str
    studio: str
    source: str
    genres: List[str] | str | None
    theme: str | None
    demographic: str | None
    sinopsis: str
    characters: List[Character]
    staff: List[Staff]
    score: float | None
    
# Clase que representa la paginación
class Pagination(BaseModel):
    prev_page: str | None
    next_page: str | None

# Clase que representa la respuesta del top de MyAnimeList
class AnimeTopResponse(BaseModel):
    message: str
    data: List[AnimeTop]
    code: int = 200
    
# Clase que representa la respuesta de los animes de temporada de MyAnimeList
class SeasonalAnimesResponse(BaseModel):
    message: str
    data: List[SeasonalAnime]
    code: int = 200
    
# Clase que representa la respuesta de la búsqueda de un anime en MyAnimeList
class BuscadorAnimeResponse(BaseModel):
    message: str
    data: List[BuscadorAnime]
    pagination: Pagination
    code: int = 200
    
# Clase que representa la respuesta de la información de un anime en MyAnimeList
class AnimeInfoResponse(BaseModel):
    message: str
    data: AnimeInfo
    code: int = 200