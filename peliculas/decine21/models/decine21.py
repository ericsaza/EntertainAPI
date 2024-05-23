from typing import List
from pydantic import BaseModel

# Clase que representa las peliculas de cada dia del calendario de Decine21
class Pelicula(BaseModel):
    title: str
    release_year: int
    duration_min: int
    synopsis: str
    url_decine: str

# Clase que representa los dias del calendario de estrenos
class Dia(BaseModel):
    day: str
    films: List[Pelicula]

# Clase que representa la respuesta del calendario de estrenos de Decine21
class CalendarioEstrenosResponse(BaseModel):
    message: str
    data: List[Dia]
    code: int = 200
    