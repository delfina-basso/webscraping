# Jupyter Notebook - Informe Técnico

Esta carpeta contiene el Jupyter Notebook con el informe técnico completo del trabajo práctico.

## Contenido del Informe

El notebook debe incluir las siguientes secciones:

### 1. Introducción

- Descripción del problema
- Objetivos del trabajo
- Tecnologías utilizadas

### 2. Análisis y Diseño

#### Parte 1: APIs

- Análisis de OpenAlex API
- Análisis de The Lens API
- Diseño de la solución
- Explicación de librerías utilizadas (requests, pandas)
- Estructuras de datos aplicadas

#### Parte 2: Web Scraping

- Análisis de los sitios web objetivo
- Diseño del scraper
- Explicación de librerías utilizadas (BeautifulSoup, requests)
- Estrategias de extracción de datos
- Estructuras de datos aplicadas

#### Parte 3: RSS Feeds

- Análisis de feeds RSS
- Diseño del parser
- Explicación de librerías utilizadas (feedparser)
- Estrategias de extracción de información
- Estructuras de datos aplicadas

#### Parte 4: Interfaz de Consola

- Diseño de la interfaz de usuario
- Integración de módulos
- Manejo de errores

### 3. Implementación

- Código relevante con explicaciones
- Ejemplos de ejecución
- Capturas de pantalla

### 4. Problemas Encontrados

- Descripción de problemas técnicos
- Soluciones implementadas
- Lecciones aprendidas

### 5. Resultados

- Archivos CSV generados
- Análisis de los datos obtenidos
- Estadísticas y visualizaciones

### 6. Conclusiones

- Reflexión sobre el trabajo realizado
- Aprendizajes del equipo
- Posibles mejoras futuras

## Estructura Recomendada

```text
notebook/
├── README.md (este archivo)
├── informe_tp.ipynb (notebook principal)
└── assets/ (opcional: imágenes, capturas, etc.)
```

## Ejecución

Para abrir el notebook:

```bash
jupyter notebook docs/notebook/informe_tp.ipynb
```

O usar JupyterLab:

```bash
jupyter lab docs/notebook/
```

## Requisitos

Asegurarse de tener instaladas las dependencias:

```bash
pip install jupyter notebook pandas matplotlib seaborn
```
