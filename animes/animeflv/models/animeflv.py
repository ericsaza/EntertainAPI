from typing import List
from pydantic import BaseModel

# Clase que representa un episodio
class Episodio(BaseModel):
    title: str
    episode: str
    image_src: str
    url: str
    
# Clase que representa uno de los últimos animes añadidos
class AnimeAnadido(BaseModel):
    title: str
    image_src: str
    sinopsis: str
    animeflv_info: str
    type: str
    score: str
    url: str
    
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
