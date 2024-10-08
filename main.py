# Importamos lo necesario para la API
from fastapi import FastAPI
from principal.routes import router as principal_router
from animes.animeflv.routes import router as animeflv_router
from animes.myanimelist.routes import router as myanimelist_router
from peliculas.decine21.routes import router as decine21_router
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

# Creamos la instancia de la API
app = FastAPI(
    title="EntertainAPI",
    description="EntertainAPI es una interfaz de programación de aplicaciones (API) diseñada para ofrecer acceso fácil y rápido a una amplia variedad de datos relacionados con entretenimiento, incluyendo información sobre películas, series, animes, mangas y más. ",
    version="1.0",
)

app.add_middleware( # Añadimos el middleware para permitir CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añadimos los routers de la API
app.include_router(principal_router, prefix="/api", tags=["Principal"]) # Añadimos el router principal
app.include_router(animeflv_router, prefix="/api/anime/animeflv", tags=["Anime/AnimeFLV (ESP)"]) # Añadimos el router de AnimeFLV
app.include_router(myanimelist_router, prefix="/api/anime/myanimelist", tags=["Anime/MyAnimeList (ENG)"]) # Añadimos el router de MyAnimeList
app.include_router(decine21_router, prefix="/api/peliculas/decine-21", tags=["Peliculas/Decine21 (ESP)"]) # Añadimos el router de Decine21

# Añadimos un endpoint para decir que la API está en "/api"
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Para ir a la api tienes que ir al endpoint de abajo.", "api" : "/api", "code": 200}

# Iniciamos la API
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
