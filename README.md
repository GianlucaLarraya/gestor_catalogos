# Cataly - Sistema de Gestión de Catálogos Digitales

## 📋 Descripción del Proyecto

**Cataly** es una aplicación web desarrollada en Django que permite a los usuarios crear, organizar y compartir catálogos digitales de fotografías. El sistema implementa un modelo de datos jerárquico (Catálogo → Álbum → Foto) con funcionalidades avanzadas de gestión de contenido y control de acceso.

### 🎯 Objetivos del Proyecto

- Desarrollar una plataforma web completa para gestión de catálogos fotográficos
- Implementar un sistema de autenticación y autorización robusto
- Crear una interfaz de usuario moderna y responsive
- Demostrar competencias en desarrollo web con Django
- Aplicar buenas prácticas de seguridad y desarrollo de software

## 🚀 Características

- **Catálogos Públicos y Privados**: Crea catálogos que puedes hacer públicos o mantener privados
- **Organización por Álbumes**: Organiza tus fotos en álbumes dentro de cada catálogo
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5 y CSS personalizado
- **Navegación Intuitiva**: Breadcrumbs y navegación entre fotos con teclado
- **Búsqueda**: Busca entre catálogos públicos
- **Gestión de Usuarios**: Sistema de autenticación integrado

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Django 4.2.21
- **Lenguaje**: Python 3.8+
- **Base de Datos**: MySQL 8.0+
- **ORM**: Django ORM

### Frontend
- **Framework CSS**: Bootstrap 5
- **Iconos**: Font Awesome
- **JavaScript**: Vanilla JS (ES6+)
- **Responsive Design**: Mobile-first approach

### Herramientas de Desarrollo
- **Gestión de Dependencias**: pip + requirements.txt
- **Variables de Entorno**: python-dotenv
- **Control de Versiones**: Git
- **Entorno Virtual**: venv

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **MySQL**: 8.0 o superior
- **Navegador**: Chrome, Firefox, Safari, Edge (versiones modernas)
- **Memoria RAM**: Mínimo 2GB recomendado
- **Espacio en Disco**: 100MB para la aplicación + espacio para imágenes

## 🚀 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone <tu-repositorio>
   cd proyecto_facultad
   ```

2. **Activar el entorno virtual**:
   ```bash
   source venv/bin/activate  # En macOS/Linux
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   ```bash
   # Copia el archivo de ejemplo
   cp .env.example .env
   
   # Edita el archivo .env con tus credenciales
   # SECRET_KEY: Genera una nueva clave secreta
   # DB_PASSWORD: Tu contraseña de MySQL
   ```

5. **Configurar la base de datos**:
   ```sql
   -- Conectar a MySQL como root
   mysql -u root -p
   
   -- Crear la base de datos
   CREATE DATABASE cataly CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- Verificar que se creó correctamente
   SHOW DATABASES;
   ```
   - Las credenciales se leen desde el archivo `.env`

6. **Ejecutar migraciones**:
   ```bash
   python manage.py migrate
   ```

7. **Crear superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Crear datos de ejemplo** (opcional):
   ```bash
   python create_sample_data.py
   ```

9. **Ejecutar el servidor**:
   ```bash
   python manage.py runserver
   ```

## 📖 Arquitectura del Sistema

### Modelo de Datos

El sistema implementa un modelo jerárquico de tres niveles:

```
Usuario
└── Catálogo (Catalog)
    ├── UUID único para identificación pública
    ├── Configuración de visibilidad (público/privado)
    └── Álbum (Album)
        ├── Organización temática de fotos
        └── Foto (Photo)
            ├── Imagen real (ImageField)
            ├── Metadatos (título, fecha de subida)
            └── Relación con álbum padre
```

### Patrón de URLs

El sistema utiliza URLs RESTful con UUIDs para catálogos:

- `/catalog/<uuid>/` - Detalle de catálogo
- `/catalog/<uuid>/album/<id>/` - Detalle de álbum
- `/catalog/<uuid>/album/<id>/photo/<id>/` - Detalle de foto

## 🌐 Funcionalidades del Frontend

### Páginas Principales

1. **Página de Inicio** (`/`):
   - Muestra catálogos públicos
   - Estadísticas generales
   - Barra de búsqueda
   - Enlaces a características principales

2. **Mis Catálogos** (`/my-catalogs/`):
   - Solo para usuarios autenticados
   - Lista todos los catálogos del usuario
   - Acciones rápidas para crear contenido
   - Gestión de catálogos existentes

3. **Búsqueda** (`/search/`):
   - Busca entre catálogos públicos
   - Sugerencias de búsqueda popular
   - Resultados filtrados

### Navegación de Contenido

1. **Detalle de Catálogo** (`/catalog/<uuid>/`):
   - Información del catálogo
   - Lista de álbumes
   - Vista previa de fotos recientes
   - Estadísticas del catálogo

2. **Detalle de Álbum** (`/catalog/<uuid>/album/<id>/`):
   - Todas las fotos del álbum
   - Información del álbum
   - Navegación de vuelta al catálogo

3. **Detalle de Foto** (`/catalog/<uuid>/album/<id>/photo/<id>/`):
   - Visor de foto a pantalla completa
   - Navegación entre fotos (flechas o teclado)
   - Información detallada de la foto
   - Enlaces de navegación

### Funcionalidades Especiales

- **Navegación con Teclado**: En la vista de foto, usa las flechas izquierda/derecha para navegar
- **Responsive Design**: Funciona perfectamente en móviles y tablets
- **Breadcrumbs**: Navegación clara en todas las páginas
- **Acceso Controlado**: Los catálogos privados solo son visibles para sus propietarios

## 👤 Gestión de Contenido

### Operaciones CRUD

El sistema implementa operaciones CRUD completas para todos los modelos:

#### Catálogos
- **Crear**: Formulario personalizado con validaciones
- **Leer**: Vista detallada con estadísticas
- **Actualizar**: Formulario de edición con permisos
- **Eliminar**: Confirmación antes de eliminar

#### Álbumes
- **Crear**: Desde el detalle del catálogo
- **Leer**: Vista de álbum con grid de fotos
- **Actualizar**: Formulario de edición
- **Eliminar**: Con confirmación y redirección

#### Fotos
- **Crear**: Subida de imágenes con validación
- **Leer**: Visor a pantalla completa con navegación
- **Actualizar**: Edición de metadatos
- **Eliminar**: Confirmación antes de eliminar

### Control de Acceso

- **Propietarios**: Acceso completo a su contenido
- **Usuarios autenticados**: Solo pueden ver catálogos públicos
- **Usuarios anónimos**: Solo pueden ver catálogos públicos
- **Superusuarios**: Acceso administrativo completo

### Usuario de Prueba

Si ejecutaste el script de datos de ejemplo:
- **Usuario**: `demo_user`
- **Contraseña**: `demo123`

## 🎨 Personalización

### Colores y Estilos

Los estilos están definidos en `catalogs/templates/catalogs/base.html`. Puedes modificar:

- Variables CSS en `:root`
- Colores principales
- Tipografías
- Espaciados y bordes

### Templates

Todos los templates están en `catalogs/templates/catalogs/`:
- `base.html`: Template base con navegación
- `home.html`: Página principal
- `catalog_detail.html`: Detalle de catálogo
- `album_detail.html`: Detalle de álbum
- `photo_detail.html`: Visor de foto
- `my_catalogs.html`: Catálogos del usuario
- `search.html`: Búsqueda
- `access_denied.html`: Acceso denegado

## 🔒 Seguridad y Configuración

### Medidas de Seguridad Implementadas

1. **Autenticación de Usuarios**
   - Sistema de login/logout integrado
   - Registro de usuarios con validaciones
   - Protección de rutas con `@login_required`

2. **Autorización y Permisos**
   - Control de acceso basado en propiedad
   - Verificación de permisos en vistas
   - Protección contra acceso no autorizado

3. **Protección de Datos**
   - Variables de entorno para configuraciones sensibles
   - Contraseñas de base de datos no hardcodeadas
   - SECRET_KEY configurada desde variables de entorno

4. **Validación de Formularios**
   - Validaciones del lado del servidor
   - Protección CSRF en todos los formularios
   - Sanitización de datos de entrada

### Configuración Avanzada

### Configuración de Variables de Entorno

El proyecto usa variables de entorno para configuraciones sensibles. Crea un archivo `.env` basado en `.env.example`:

```bash
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Database Settings
DB_NAME=cataly
DB_USER=root
DB_PASSWORD=tu-contraseña-de-base-de-datos
DB_HOST=localhost
DB_PORT=3306
```

**⚠️ Importante**: Nunca subas el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

### Configuración de Base de Datos

La configuración de la base de datos se lee automáticamente desde las variables de entorno en `cataly/settings.py`.

## 📊 Estructura del Proyecto

```
proyecto_facultad/
├── cataly/                 # Configuración principal de Django
│   ├── settings.py        # Configuración del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── catalogs/             # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de negocio
│   ├── urls.py           # URLs de la aplicación
│   ├── admin.py          # Configuración del admin
│   └── templates/        # Templates HTML
├── media/                # Archivos de medios subidos
├── venv/                 # Entorno virtual
├── requirements.txt      # Dependencias del proyecto
├── .env                  # Variables de entorno (no en git)
├── .env.example          # Plantilla de variables de entorno
└── README.md            # Documentación del proyecto
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Gianluca Larraya**
- Estudiante de Ingeniería Informática