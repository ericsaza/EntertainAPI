from typing import List
from pydantic import BaseModel

# Clase que representa las fechas de inicio y fin de un anime del top de MyAnimeList
class Dates(BaseModel):
    start_date: str
    end_date: str

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
    synopsis: str
    score: float | None
    url_mal: str
    url_api: str 

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