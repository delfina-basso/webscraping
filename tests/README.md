# Casos de Prueba

Esta carpeta contiene todos los casos de prueba del proyecto.

## Estructura

- `test_api.py` - Pruebas del módulo de APIs
- `test_scraping.py` - Pruebas del módulo de web scraping
- `test_rss.py` - Pruebas del módulo RSS
- `test_interfaz.py` - Pruebas de la interfaz de consola

## Requisitos

Se deben implementar pruebas que cubran:

1. **Consultas a APIs**
   - Conexión exitosa a OpenAlex
   - Conexión exitosa a The Lens
   - Extracción de metadatos correctos
   - Manejo de errores de red

2. **Web Scraping**
   - Scraping de eventseye.com
   - Scraping de nferias.com
   - Scraping de 10times.com
   - Manejo de páginas no disponibles

3. **Procesamiento RSS**
   - Lectura de feeds de WTO
   - Lectura de feeds de UN Comtrade
   - Parsing correcto de XML
   - Extracción de información de noticias

4. **Persistencia de Datos**
   - Generación correcta de archivos CSV
   - Formato de datos consistente
   - Manejo de caracteres especiales

5. **Interfaz de Usuario**
   - Menú interactivo funcional
   - Validación de entradas
   - Manejo de errores de usuario

6. **Casos Límite**
   - Manejo de respuestas vacías
   - Timeout de conexiones
   - Datos malformados

## Ejecución

Para ejecutar todas las pruebas:

```bash
pytest tests/
```

Para ejecutar pruebas con coverage:

```bash
pytest --cov=src tests/
```

Para ejecutar un módulo específico:

```bash
pytest tests/test_api.py
```

## Framework de Testing

Se recomienda usar:
- `pytest` para las pruebas
- `unittest.mock` para simular llamadas a APIs
- `pytest-cov` para análisis de cobertura
