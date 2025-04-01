# MISO - Sancochof - DevOps 202512

### Comenzando

Requisitos: Python 3.10 o superior

### En local

1. Crear un entorno virtual:

```sh
python3 -m venv env
```

2. Activar entorno:

```sh
source env/bin/activate
```

3. Instalar dependencias:

```sh
pip install -r requirements.txt
```

4. Crear variable de entorno

Copie el archivo `.env.template` y renómbrelo `.env.development`. Luego asigne los valores.

5. Levantar aplicación:

```sh
flask --app application run
```

#### Desde Docker

1. Iniciar servicios

```sh
docker compose up
```


### Desplegando en AWS

Crear `.zip` con el contenido de la carpeta y subirlo al entorno de EB.

```sh
zip -r deploy.zip . -x "*.git*" "__pycache__/*" "env/*" "*.venv/*" "*.DS_Store"
```


#### Integrantes

- Jhorman Galindo
- Leiner Barrios
- Alejandro Bogotá
- Jaime Gallo
