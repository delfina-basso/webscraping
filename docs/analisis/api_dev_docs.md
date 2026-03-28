# API Developement

## Diseño general
Vamos a usar una clase genérica que se llame `APIClient` que se inicialize:

1. **Clase `APIClient` (en `src/api/`):**
   - **Métodos:**
     - `consultar_por_tema(tema: str, limite: int) -> list[int]`
       - Consulta artículos/patentes relacionados con un tema.
       - **Recibe:** Tema de búsqueda y límite de resultados.
       - **Devuelve:** Lista con ID de los artículos.
     - `consultar_generales(limite: int) -> list[int]`
       - Consulta los últimos artículos/patentes publicados.
       - **Recibe:** Límite de resultados.
       - **Devuelve:** Lista con ID de los artículos.
     - `extrar_metadatos(lista_IDs_articulos: int) -> list[dict]`
       - De una lista de artículos (por ID) se busca todos los metadatos solicitados.
       - **Recibe:** Lista de IDs de aríticulos académicos (ver si esto cambio según API, si es el caso falta algun indicativo).
       - **Devuelve:** Lista de diccionarios con metadata de los artículos solicitados.

De la Clase de arriba en realidad, extrar metadato lo uso en las 2 sub métodos, pero va para los dos.

Agregar a esta clase un chequeo del estado de la API.

Esta data puede pasar a un chequeo general (no se si gestionarlo general o que cada uno haga su chequeo). Y de ahí a una clase CSV para guardar la data.

2. **Clase `CSVUtils` (en `src/estructuras/`):**
   - **Métodos:**
     - `save_csv(category: string, input: dict) -> csv file`
       - Crea el csv en base al diccionario con información.
       - **Recibe:** Categorías (ej, "Artículo científico") y el diccionario con la data.
       - **Devuelve:** Nada. Guarda el CSV con el nombre correspondiente.
     - `read_csv() -> dict`
       - Consulta los últimos artículos/patentes publicados.
       - **Recibe:** Límite de resultados.
       - **Devuelve:** Lista de diccionarios con metadatos.

## Interacción con la API
Voy a hacer un .py para cada web, y ahí resuelvo cada sub tarea.
Para OpenAlex, tengo que primero buscar los 50 artículos por palabra clave, y con esos ID itero para sacar la data. Las llamadas generales (lógica general, primero buscar 50 artículos, después buscar cada info en concreto, lo puedo hacer en la clase de API client).

## Data general
- Lo resolvemos todo con clases o con funciones (después va a ser un quilombo sino)
- Lo unico que puede ir a estructuras es el formato para guardar en CSV (así todos usamos el mismo)
- Tal vez un chequeo de que la data sea válida general? O mucho quilombo?
