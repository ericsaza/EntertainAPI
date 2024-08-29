Español | [Inglés](https://github.com/ericsaza/EntertainAPI/blob/main/README.md)

# EntertainAPI
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#descripción-general">Descripción general</a>
    </li>
    <li>
      <a href="#instalación">Instalación</a>
    </li>
    <li>
      <a href="#apis">APIs</a>
    </li>
    <li>
      <a href="#documentación-api">Documentación API</a>
    </li>
  </ol>
</details>

## Descripción general
EntertainAPI es una interfaz de programación de aplicaciones (API) diseñada para ofrecer acceso fácil y rápido a una amplia variedad de datos relacionados con entretenimiento, incluyendo información sobre películas, series, animes, mangas y más. Los datos son obtenidos mediante scraping de cada página web utilizando BeautifulSoup.

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/jorgeajimenezl/animeflv-api.git
   ```

2. Navega al directorio del repositorio clonado:
   ```sh
   cd EntertainAPI
   ```

3. Instala las dependencias necesarias:
   ```sh
   pip install -r requirements.txt
   ```

4. Instala el paquete:
   ```sh
   pip install .
   ```

## APIs
### Animes
- **AnimeFLV (ESP)**: API para obtener información sobre animes en español desde AnimeFLV.
- **MyAnimeList (ENG)**: API para obtener información sobre animes en inglés desde MyAnimeList.

### Películas
- Decine21 (ESP): API para obtener información sobre películas desde Decine21.


## Documentación API
La documentación de EntertainAPI está disponible en dos formatos:
- **Swagger UI:** Puedes acceder a la documentación interactiva a través del endpoint `/doc`.
![688shots_so](https://github.com/ericsaza/EntertainAPI/assets/94136968/f2e0d64d-6877-4383-84af-0286caa81619)

- **ReDoc**: Puedes acceder a la documentación alternativa y detallada a través del endpoint `/redoc`.
![376shots_so](https://github.com/ericsaza/EntertainAPI/assets/94136968/536f8c7f-86f2-45b0-ab61-0f0e4e3a0c30)
