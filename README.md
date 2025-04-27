# Backend Spendr (be-spendr)

Backend para la aplicación Spendr, encargado de gestionar la lógica de negocio, la autenticación de usuarios y la interacción con la base de datos para el seguimiento de gastos e ingresos.

## Tabla de Contenidos

-   [Prerrequisitos](#prerrequisitos)
-   [Instalación](#instalación)
-   [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
-   [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
-   [Cómo Funciona](#cómo-funciona)
-   [Rutas del API (Endpoints)](#rutas-del-api-endpoints)
-   [Variables de Entorno Necesarias](#variables-de-entorno-necesarias)
-   [Tecnologías Utilizadas](#tecnologías-utilizadas)

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

-   [Python 3](https://www.python.org/) (Se recomienda la versión 3.11 o superior)
-   Una instancia de base de datos [MongoDB](https://www.mongodb.com/).
-   (Opcional) [Docker](https://www.docker.com/) si el proyecto está configurado para ejecutarse en contenedores.

---

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/DanMarqz/be-spendr.git
   cd be-spendr
   ```
2. Crea un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz del proyecto (ver sección [Variables de Entorno](#-variables-de-entorno)).

---

## Configuración de Variables de Entorno

Este proyecto requiere ciertas variables de entorno para funcionar correctamente (conexión a base de datos, secretos, etc.).

1.  **Crea un archivo `.env`:**
    Busca un archivo llamado `.env.example` o similar en la raíz del proyecto. Si existe, cópialo para crear tu propio archivo `.env`:
    ```bash
    cp .env.example .env
    ```
    Si no existe un archivo `.env.example`, necesitarás crear el archivo `.env` manualmente.

2.  **Edita el archivo `.env`:**
    Abre el archivo `.env` con un editor de texto y rellena los valores correspondientes para cada variable. Consulta la sección [Variables de Entorno Necesarias](#variables-de-entorno-necesarias) para más detalles.

    *Ejemplo de contenido del archivo `.env` (los nombres reales pueden variar):*
    ```plaintext
    PORT=3000
    DATABASE_URL=mongodb://localhost:27017/spendr_db # O las variables específicas de tu DB
    APP_SECRET_KEY=tu_secreto_muy_seguro_para_jwt
    # Otras variables que puedan ser necesarias...
    ```

---

## Ejecución de la Aplicación

- Para correr la aplicación localmente:
  ```bash
  python main.py
  ```
- También puedes construir la imagen Docker y correrla:
  ```bash
  docker build -t spendr-backend .
  docker run -p 8000:8000 --env-file .env spendr-backend
  ```

---

## Cómo Funciona

El backend de Spendr es una API RESTful construida probablemente con Python y Flask. Sus responsabilidades principales incluyen:

1.  **Autenticación y Autorización:** Maneja el registro de nuevos usuarios, el inicio de sesión y protege las rutas para asegurar que solo los usuarios autenticados puedan acceder a sus propios datos.
2.  **Gestión de Datos (CRUD):** Proporciona endpoints para Crear, Leer, Actualizar y Eliminar (CRUD) recursos como:
    * Transacciones (gastos e ingresos)
    * Categorías de transacciones
    * Presupuestos
    * Cuentas de usuario
3.  **Lógica de Negocio:** Puede incluir cálculos de balances, resúmenes financieros, validaciones de datos, etc.
4.  **Interacción con la Base de Datos:** Se comunica con la base de datos para persistir y recuperar la información del usuario y sus finanzas.

La aplicación sigue una arquitectura común de backend donde las solicitudes HTTP llegan a las rutas definidas, son procesadas por controladores que interactúan con modelos (representación de los datos) y servicios (lógica de negocio), y finalmente devuelven una respuesta JSON al cliente (frontend, aplicación móvil).

- La estructura principal:
  - `controllers/`: define las rutas (endpoints).
  - `services/`: contiene la lógica de negocio.
  - `utils/`: utilidades como validaciones y manejo de contraseñas.
- El flujo básico:
  - El cliente envía peticiones HTTP (gastos, ingresos, autenticación).
  - Se procesan en los controladores y se valida la información.
  - Los servicios ejecutan operaciones (como crear usuarios, añadir gastos).
  - La respuesta se devuelve al cliente en formato JSON.

---

## Rutas del API (Endpoints)

A continuación se describen las rutas principales del API.

| Método | Ruta                      | Función                                               |
|:------:|:-------------------------:|:-----------------------------------------------------:|
| GET    | `/status`                 | Obtiene el estado actual de la aplicación.            |
| GET    | `/test-db-connection`     | Valida la conexión a la base de datos.                |
| GET    | `/`                       | Ruta raíz, usada para visualizar todos los gastos.    |
| GET    | `/{id}`                   | Obtener un todo por ID (parece endpoint de prueba).   |
| POST   | `/auth/login`             | Autenticar usuario y devolver un token JWT.           |
| POST   | `/auth/register`          | Registrar un nuevo usuario.                           |
| POST   | `/auth/logout`            | Cerrar sesión del usuario.                            |

---

## Variables de Entorno Necesarias

Debes definir un archivo `.env` con las siguientes variables:

| Variable        | Descripción                                  |
|:----------------|:--------------------------------------------|
| `SECRET_KEY`    | Clave secreta para firmar el token JWT       |
| `ERROR_MSG`     | Mensaje para debuguear errores...    |
| `DB_NAME`       | Nombre de la base de datos de Mongo |
| `DATABASE_URL`  | URL de conexión a la base de datos SQLite o PostgreSQL |

### Ejemplo de `.env`:

```dotenv
SECRET_KEY=SECRET_KEY
ERROR_MSG='~~~~ An error occurred while trying to...'
DB_NAME=DB_NAME
DB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
```

---

## Tecnologías Utilizadas

- **Python 3.11+**
- **Flask**
- **Docker** (opcional para contenerización)

