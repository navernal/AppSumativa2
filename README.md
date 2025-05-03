# App Sumativa 2

Este proyecto usa **Docker Compose** para levantar una base de datos Oracle y **Django** como backend.

## Pasos para ejecutar el proyecto

1. **Levantar la base de datos**:

    Primero, ejecuta el siguiente comando para levantar el contenedor de la base de datos Oracle:

    ```bash
    docker-compose up -d
    ```

2. **Realizar migraciones en Django**:

    Una vez que la base de datos esté en marcha, ejecuta las migraciones de Django:

    ```bash
    python manage.py migrate
    ```


3. **Ejecutar el servidor Django**:

    Finalmente, levanta el servidor de desarrollo de Django:

    ```bash
    python manage.py runserver
    ```

    El servidor estará disponible en `http://127.0.0.1:8000`.

## Comandos útiles

- **Detener los contenedores de Docker**:

    ```bash
    docker-compose down
    ```

