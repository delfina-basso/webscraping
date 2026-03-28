# Código Fuente

Esta carpeta contiene todo el código fuente del proyecto organizado por módulos.

## Estructura del Proyecto

### Módulos Principales

- `api/` - Consultas a APIs de OpenAlex y The Lens
- `scraping/` - Web scraping de eventos y ferias
- `rss/` - Procesamiento de feeds RSS para noticias
- `interfaz/` - Interfaz de consola interactiva

### Módulos de Soporte

- `estructuras/` - Implementación de estructuras de datos personalizadas
- `utils/` - Utilidades y funciones auxiliares

## Técnicas Utilizadas

### 1. APIs (Parte 1)

- OpenAlex API para artículos científicos
- The Lens API para patentes
- Manejo de requests HTTP
- Parsing de respuestas JSON

### 2. Web Scraping (Parte 2)

- BeautifulSoup para análisis de HTML
- Scraping ético respetando robots.txt
- Manejo de paginación y contenido dinámico

### 3. RSS Feeds (Parte 3)

- Feedparser para lectura de feeds RSS
- Procesamiento de XML
- Extracción de metadatos

### 4. Estructuras de Datos

- Listas, diccionarios, conjuntos
- Estructuras personalizadas según necesidad
- Análisis de complejidad algorítmica

## Ejecución

Para ejecutar el programa principal:

```bash
python main.py
```

Para instalar dependencias:

```bash
pip install -r requirements.txt
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest tests/
```
