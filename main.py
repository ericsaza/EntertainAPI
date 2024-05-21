# Importamos lo necesario para la API
from fastapi import FastAPI
from principal.routes import router as principal_router
import uvicorn

# Creamos la instancia de la API
app = FastAPI(
    title="EntertainAPI",
    description="EntertainAPI es una interfaz de programación de aplicaciones (API) diseñada para ofrecer acceso fácil y rápido a una amplia variedad de datos relacionados con entretenimiento, incluyendo información sobre películas, series, animes, mangas y más. ",
    version="1.0",
)

# Añadimos los routers de la API
app.include_router(principal_router, prefix="/api", tags=["Principal"])

# Iniciamos la API
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
