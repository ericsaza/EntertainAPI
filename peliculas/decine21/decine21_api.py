from enum import Enum
from fastapi import Query
from utils.scrap_utils import *

class EnumMeses(str, Enum):
    enero = "enero"
    febrero = "febrero"
    marzo = "marzo"
    abril = "abril"
    mayo = "mayo"
    junio = "junio"
    julio = "julio"
    agosto = "agosto"
    septiembre = "septiembre"
    octubre = "octubre"
    noviembre = "noviembre"
    diciembre = "diciembre"

class Decine21API:
    
    # Endpoint para ver la información de la API de Decine21
    def info_endpoint(self):
        return {
            "message": "Endpoint para ver la información de la API de Decine21.",
            "description": "En este endpoint se puede ver la información de la API de Decine21, la cual es una API de entretenimiento que ofrece acceso a una amplia variedad de datos relacionados con películas, series, animes, mangas y más.",
            "endpoints": {
            },
            "other_film_endpoints": {
                "calendario_estrenos": "/api/peliculas/decine-21/calendario-estrenos?ano=2024&mes=enero",
            },
            "documentation": {"swagger": "/docs", "doc": "/redoc"},
            "code": 200,
        }
        
    # Endpoint para ver el calendario de estrenos de Decine21
    def calendario_estrenos(self, ano: int = Query(..., example=2024, description="Año de los estrenos a buscar.", gt=0, lt=3000), mes: EnumMeses = Query(..., example=EnumMeses.enero, description="Mes de los estrenos a buscar.")):
        
        num_mes = "01"
        
        # Dependiendo del mes de da un número u otro
        if mes == EnumMeses.enero:
            num_mes = "01"
        elif mes == EnumMeses.febrero:
            num_mes = "02"
        elif mes == EnumMeses.marzo:
            num_mes = "03"
        elif mes == EnumMeses.abril:
            num_mes = "04"
        elif mes == EnumMeses.mayo:
            num_mes = "05"
        elif mes == EnumMeses.junio:
            num_mes = "06"
        elif mes == EnumMeses.julio:
            num_mes = "07"
        elif mes == EnumMeses.agosto:
            num_mes = "08"
        elif mes == EnumMeses.septiembre:
            num_mes = "09"
        elif mes == EnumMeses.octubre:
            num_mes = "10"
        elif mes == EnumMeses.noviembre:
            num_mes = "11"
        elif mes == EnumMeses.diciembre:
            num_mes = "12"
        
        
        # Obtenemos el contenido de la URL
        soup = obtener_contenido_url(f"https://decine21.com/estrenos/cine/?fecha={ano}{num_mes}")
        
        # Primero obtenemos los días
        dias = []
        for dia in guardar_varios_elementos_por_tag_y_atributo(soup, "div", "class", "card shadow my-5"):
            name_dia = obtener_texto_elemento_buscado_por_tag_y_atributo(dia, "h2", "class", "h5 asdsgf m-0 text-secondary font-weight-bold")
            
            # Ahora obtenemos las películas
            peliculas = []
            for pelicula in guardar_varios_elementos_por_tag_y_atributo(dia, "div", "class", "list-film"):
                title = obtener_texto_elemento_buscado_por_tag_y_atributo(pelicula, "h3", "class", "h5")
                
                # Controlamos si el año de estreno está en el título
                try:
                    ano_estr = guardar_elemento_por_tag_y_atributo(pelicula, "div", "class", "list-film-data d-flex justify-content-between").find("strong").text.replace("(", "").replace(")", "")
                except:
                    ano_estr = None
                duracion = obtener_texto_elemento_buscado_por_tag_y_atributo(pelicula, "span", "class", "d-none d-lg-inline-block").split(" ")[1]
                sinopsis = obtener_texto_elemento_buscado_por_tag_y_atributo(pelicula, "div", "class", "list-film-sinopsis")
                url_decine = guardar_elemento_por_tag_y_atributo(pelicula, "h3", "class", "h5").find("a")["href"]
                decine_id = url_decine.split("-")[-1]
                
                # Añadimos la película a la lista
                peliculas.append({
                    "decine_id": decine_id,
                    "title": title,
                    "release_year": ano_estr,
                    "duration_min": duracion,
                    "synopsis": sinopsis,
                    "url_decine": f'https://decine21.com/{url_decine}'
                })
            
            dias.append({
                "day": name_dia,
                "films": peliculas
            })
        
        return {
            "message": "Endpoint para ver el calendario de estrenos de Decine21.",
            "data": dias,
            "code": 200,
        }