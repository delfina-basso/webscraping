# Estructura del Proyecto - Recuperación de Información en la Web

## 📁 Organización Completa del Espacio de Trabajo

A continuación se detalla la estructura completa del proyecto, incluyendo código fuente, documentación, casos de prueba y organización del trabajo en equipo.

Esta estructura está diseñada para facilitar la colaboración entre los integrantes del grupo, permitiendo que cada uno pueda trabajar en su módulo asignado y contribuir al proyecto de manera organizada.

> [!TIP]
> Pueden modificar la estructura del proyecto y adaptarla a sus necesidades.
>
> Se recomienda mantener una estructura clara y coherente para facilitar la colaboración.
>
> Se recomienda crear un entorno virtual de Python para trabajar con este proyecto.

```text
tp-2025/
├── README.md                    # Descripción general del trabajo práctico
├── .gitignore                   # Archivos ignorados por git
├── ESTRUCTURA_PROYECTO.md       # Este archivo
│
├── 📁 src/                      # Código fuente principal
│   ├── README.md
│   ├── api/                     # Módulo para consultas a APIs (OpenAlex, The Lens)
│   ├── scraping/                # Módulo de web scraping (eventos y ferias)
│   ├── rss/                     # Módulo de procesamiento RSS (noticias)
│   ├── interfaz/                # Interfaz de consola
│   ├── estructuras/             # Estructuras de datos personalizadas
│   └── utils/                   # Utilidades y funciones auxiliares
│
├── 📁 docs/                     # Documentación técnica
│   ├── README.md
│   ├── analisis/                # Análisis de diseño y técnicas
│   ├── diagramas/               # Diagramas de arquitectura
│   ├── presentacion/            # Material para presentación oral
│   └── notebook/                # Jupyter Notebooks (.ipynb)
│
├── 📁 tests/                    # Casos de prueba
│   ├── README.md
│   ├── test_api.py              # Pruebas del módulo de APIs
│   ├── test_scraping.py         # Pruebas del módulo de scraping
│   ├── test_rss.py              # Pruebas del módulo RSS
│   └── test_interfaz.py         # Pruebas de la interfaz
│
├── 📁 data/                     # Datos generados (archivos CSV)
│   ├── .gitkeep                 # Mantener directorio en git
│   ├── articulos.csv            # Artículos científicos
│   ├── patentes.csv             # Patentes
│   ├── eventos.csv              # Eventos y ferias
│   └── noticias.csv             # Noticias de comercio internacional
│
├── main.py                      # Punto de entrada principal
└── requirements.txt             # Dependencias de Python
```

## 🎯 Módulos del Sistema

### Módulos Principales

1. **`api/`** - Consultas a APIs de OpenAlex y The Lens
   - Obtención de artículos científicos
   - Obtención de patentes
   - Extracción de metadatos
   - Persistencia en CSV

2. **`scraping/`** - Web scraping de eventos y ferias
   - Scraping de eventseye.com
   - Scraping de nferias.com
   - Scraping de 10times.com
   - Consolidación en un único CSV

3. **`rss/`** - Procesamiento de feeds RSS
   - Lectura de feeds de WTO
   - Lectura de feeds de UN Comtrade
   - Extracción de información de noticias
   - Persistencia en CSV

4. **`interfaz/`** - Interfaz de consola
   - Menú interactivo
   - Opciones de consulta
   - Visualización de resultados

### Módulos de Soporte

5. **`estructuras/`** - Estructuras de datos personalizadas

6. **`utils/`** - Funciones auxiliares y utilidades

## 📋 Entregables Organizados

- **📄 Código fuente**: Organizado por módulos en `src/`
- **📚 Documentación técnica**: En `docs/` con análisis y diseño
- **📓 Jupyter Notebook**: Informe completo en `docs/notebook/`
- **🧪 Casos de prueba**: Tests en `tests/`
- **📊 Datos generados**: Archivos CSV en `data/`
- **🎤 Presentación oral**: Material en `docs/presentacion/`

## 👥 Trabajo en Equipo

- **Roles definidos**: Cada integrante tiene responsabilidades específicas
- **Seguimiento**: Plantillas para reuniones y planificación
- **Colaboración**: Estructura que facilita el trabajo distribuido
- **Commits identificables**: Cada integrante puede trabajar en su módulo

## 🏗️ Próximos Pasos

1. **Asignar roles** específicos a cada integrante del grupo
2. **Completar información** en `equipo/README.md`
3. **Instalar dependencias** con `pip install -r requirements.txt`
4. **Definir cronograma** detallado en `equipo/planificacion/`
5. **Comenzar implementación** con módulos básicos

## 📚 Requisitos Técnicos

- **Lenguaje**: Python 3.8+
- **Librerías principales**:
  - `requests` - Consultas HTTP a APIs y scraping
  - `beautifulsoup4` - Análisis de HTML
  - `feedparser` - Lectura de RSS
  - `pandas` - Manipulación de datos y exportación a CSV
  - `jupyter` - Para el informe en notebook

---

**✅ El entorno está configurado y listo para el desarrollo colaborativo del trabajo práctico grupal.**
