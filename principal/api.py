# Creamos la clase principal de la API
class PrincipalAPI:
    
    # Método para la ruta principal de la API
    def hola_mundo(self): # el "self" es necesario para que FastAPI pueda reconocer el método
        return {"mensaje": "Hola Mundo"}