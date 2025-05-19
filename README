# Portal practicas

## Requirimientos
- Python 3.9+
- Dependencias listadas en requirements.txt

## Inicialización del Proyecto

### 1. Clonar el Repositorio

```bash
git clone https://github.com/amadorssa/db-crud-project.git
cd db-crud-project
```

### 2. Configurar el Backend

1. Navega a la carpeta del backend:
   ```bash
   cd app/
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv env
   source env/bin/activate  # En macOS/Linux
   .\env\Scripts\activate  # En Windows
   cd app/
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la carpeta `backend/` para configurar las variables de entorno 
   necesarias (por ejemplo, conexión a base de datos):

   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   SECRET_KEY=supersecretkey
   ```

4. Conectar a la base de datos:
   - Asegúrate de que la base de datos esté en funcionamiento y accesible.
   ```bash
   brew services start postgresql
   psql postgres
   CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD 'postgres';
   CREATE DATABASE internships_db;
   ```

5. Inicia el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```

6. Accede a la API en:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
