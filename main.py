# Importamos lo necesario para la API
from fastapi import FastAPI
import uvicorn

# Creamos la instancia de la API
app = FastAPI()

# Creamos una ruta básica para comprobar que la API funciona
@app.get("/")
def hola_mundo():
    return {"mensaje": "Hola Mundo"}

# Iniciamos la API
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)