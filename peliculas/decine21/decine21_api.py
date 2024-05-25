from enum import Enum
from fastapi import Query
from utils.scrap_utils import *

# Enum para los meses
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
    
# Enum para las distintas plataformas de streaming
class EnumPlataformas(str, Enum):
    netflix = "netflix"
    apple_tv = "apple tv"
    hbo_max = "hbo max"
    amazon = "amazon prime video"
    movistar = "movistar+"
    disney = "disney+"
    filmin = "filmin"
    flixole = "flixolé"
    acontra = "acontra+"
    sky_showtime = "skyshowtime"

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
                "ultimo_streaming": "/api/peliculas/decine-21/ultimo-streaming?plataforma=netflix",
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
        
    # Endpoint para ver lo último en streaming de distintas plataformas
    def lo_ultimo_en_streaming(self, plataforma: EnumPlataformas = Query(..., example=EnumPlataformas.netflix, description="Plataforma de streaming a buscar.")):
        
        # Dependiendo de la plataforma se busca una URL u otra
        plataforma_url = ""
        
        if plataforma == EnumPlataformas.netflix:
            plataforma_url = "netflix"
        elif plataforma == EnumPlataformas.apple_tv:
            plataforma_url = "apple-tv"
        elif plataforma == EnumPlataformas.hbo_max:
            plataforma_url = "hbo"
        elif plataforma == EnumPlataformas.amazon:
            plataforma_url = "amazon-prime-video"
        elif plataforma == EnumPlataformas.movistar:
            plataforma_url = "movistar"
        elif plataforma == EnumPlataformas.disney:
            plataforma_url = "disney-plus"
        elif plataforma == EnumPlataformas.filmin:
            plataforma_url = "filmin"
        elif plataforma == EnumPlataformas.flixole:
            plataforma_url = "flixole"
        elif plataforma == EnumPlataformas.acontra:
            plataforma_url = "acontra"
        elif plataforma == EnumPlataformas.sky_showtime:
            plataforma_url = "skyshowtime"
            
        # Obtenemos el contenido de la URL
        soup = obtener_contenido_url(f"https://decine21.com/streaming/{plataforma_url}")
        
        # Obtenemos las películas
        peliculas = []
        
        for pelicula in guardar_varios_elementos_por_tag_y_atributo(soup, "div", "class", "caratula mostrar col-6 col-md-6 col-lg-3"):
            
            # Obtenemos los datos de la película
            title = guardar_elemento_por_tag_y_atributo(pelicula, "a", "class", "mod-articles-category-title link-unstyled").find("span").get_text(strip=True)
            image_url = guardar_elemento_por_tag_y_atributo(pelicula, "img", "class", "img-fluid shadow")["src"]
            decine_url = obtener_atributo_elemento_buscado_por_tag_y_atributo(pelicula, "a", "class", "mod-articles-category-title link-unstyled", "href")
            decine_id = decine_url.split("-")[-1]
            
            # Controlamos si la película tiene fecha de estreno
            try:
                fecha_estreno_plataforma = guardar_elemento_por_tag_y_atributo(pelicula, "span", "class", "mod-articles-category-date").get_text(strip=True)
            except:
                fecha_estreno_plataforma = None
                
            # Controlamos si la película tiene trailer
            try:
                trailer_url = f'https://decine21.com{guardar_elemento_por_tag_y_atributo(pelicula, "div", "class", "tab-item-trailer").find("a").get("href")}'
            except:
                trailer_url = None
            
            # Añadimos la película a la lista
            peliculas.append({
                "decine_id": decine_id,
                "title": title,
                "image_url": image_url,
                "release_platform_date": fecha_estreno_plataforma,
                "url_trailer": trailer_url,
                "url_decine": f'https://decine21.com{decine_url}'
            })
            

        return {
            "message": "Endpoint para ver lo último en streaming de Decine21.",
            "data": peliculas,
            "other_platforms": {
                "netflix": "/api/peliculas/decine-21/ultimo-streaming?plataforma=netflix",
                "apple_tv": "/api/peliculas/decine-21/ultimo-streaming?plataforma=apple tv",
                "hbo_max": "/api/peliculas/decine-21/ultimo-streaming?plataforma=hbo max",
                "amazon": "/api/peliculas/decine-21/ultimo-streaming?plataforma=amazon prime video",
                "movistar": "/api/peliculas/decine-21/ultimo-streaming?plataforma=movistar%2B",
                "disney": "/api/peliculas/decine-21/ultimo-streaming?plataforma=disney%2B",
                "filmin": "/api/peliculas/decine-21/ultimo-streaming?plataforma=filmin",
                "flixole": "/api/peliculas/decine-21/ultimo-streaming?plataforma=flixol%C3%A9",
                "acontra": "/api/peliculas/decine-21/ultimo-streaming?plataforma=acontra%2B",
                "sky_showtime": "/api/peliculas/decine-21/ultimo-streaming?plataforma=skyshowtime",
            },
            "code": 200,
        }