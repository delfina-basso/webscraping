<!-- markdownlint-disable MD033 MD041 -->

<p align="center"><img src="./images/untref-logo.svg" alt="UNTreF" /></p>

# Trabajo práctico grupal: Recuperación de información en la Web

**Fecha de presentación:** 25 y 27 de Noviembre

## Objetivo general

El objetivo de este trabajo es que los estudiantes apliquen conceptos de **estructuras de datos** y técnicas de **recuperación de información en la Web** (APIs, web scraping y RSS). El producto final será un programa en **Python** que extraiga, organice y persista información en archivos **CSV**, acompañado de un informe técnico y una exposición oral.

## Organización del trabajo

### Formación de grupos

- Equipos de 3 a 4 integrantes (sin excepción).

### Distribución de tareas

- Cada integrante debe asumir responsabilidades específicas (por ejemplo: manejo de APIs, scraping, procesamiento de RSS, persistencia de datos, documentación).

### Control de versiones

- El proyecto debe mantenerse en un repositorio compartido. Todos los integrantes deben realizar _commits_ frecuentes y descriptivos.
- Si un estudiante no tiene _commits_, se considerará que no participó activamente.

## Descripción del problema

Se debe desarrollar un programa en Python que procese información de distintas fuentes de la Web, aplicando técnicas diferentes en cada caso y almacenando los resultados en archivos CSV.

### Parte 1: Consulta de artículos y patentes por API

Utilizando las APIs de [OpenAlex](https://openalex.org/) y [The Lens](https://www.lens.org/), construir un _script_ que permita:

- Consultar los últimos 50 artículos científicos y patentes relacionados con un tema específico (por ejemplo: Inteligencia Artificial, Energías Renovables).
- Consultar los últimos 100 artículos y patentes publicados en general.
- Extraer los siguientes metadatos:
  - ID del artículo/patente
  - Título
  - Autores
  - Fecha y año de publicación
  - Resumen
  - Tipo de publicación
  - País de publicación
  - Campos de estudio
  - Palabras clave
  - Institución del autor e ID de institución
- Guardar los datos en un archivo CSV.

### Parte 2: Extracción de eventos y ferias mediante _Web Scraping_

Implementar un _**web scraper**_ para obtener información de los siguientes sitios:

- [https://www.eventseye.com/](https://www.eventseye.com/)
- [https://www.nferias.com/](https://www.nferias.com/)
- [https://10times.com/](https://10times.com/)

El programa debe extraer:

- Nombre del evento
- Descripción
- Fecha
- Ubicación
- Sector / industrias relacionadas
- Web oficial
- Correo de contacto (si está disponible)

Toda la información consolidada debe guardarse en un único archivo CSV.

### Parte 3: Consulta de noticias sobre comercio internacional mediante _RSS_

Procesar _**feeds RSS**_ de las siguientes fuentes:

- [https://www.wto.org/](https://www.wto.org/)
- [https://comtradeplus.un.org/](https://comtradeplus.un.org/)

El programa debe obtener:

- Título
- Fecha de publicación
- Resumen
- País asociado a la noticia

Los resultados deben almacenarse en un archivo CSV.

### Parte 4: Interfaz por consola

Crear una interfaz de consola con un menú de opciones que permita, como mínimo:

- Consultar artículos
- Consultar patentes
- Consultar próximos eventos y ferias
- Consultar últimas noticias de comercio exterior

### [OPCIONAL] Parte 5: Aplicación Web

Opcionalmente, si completaron los puntos anteriores y disponen de tiempo, pueden integrar el desarrollo en una aplicación web sencilla utilizando un framework de Python (por ejemplo, Django o Flask), replicando las opciones de la interfaz de consola.

## Requisitos Técnicos

- Lenguaje: Python
- Librerías recomendadas:
  - **requests** (consultas HTTP a APIs y scraping)
  - **BeautifulSoup** (análisis de HTML)
  - **feedparser** (lectura de RSS)
  - **pandas** (manipulación de datos y exportación a CSV)

## Entregables

1. **Código fuente** en un repositorio (todo el grupo debe tener _commits_).
2. **Informe en Jupyter Notebook (.ipynb)** que incluya:
   - Análisis y diseño de cada técnica.
   - Explicación de librerías utilizadas.
   - Descripción de estructuras de datos aplicadas.
   - Problemas encontrados y cómo se resolvieron.
   - Conclusiones y aprendizajes.
   - Archivos CSV generados.
3. **Presentación oral** (10-15 minutos).
