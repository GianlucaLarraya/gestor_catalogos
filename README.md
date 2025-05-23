# Cataly

**Cataly** es una aplicación web desarrollada con Django y MySQL que permite a los usuarios crear, organizar y compartir catálogos de fotos.  
El proyecto implementa una arquitectura limpia, separando la lógica en modelos, servicios y repositorios, y está preparado para futuras extensiones de frontend o API.

---

## Funcionalidades implementadas

- **Gestión de Catálogos**
  - Los usuarios pueden tener múltiples catálogos personales.
  - Cada catálogo tiene título, descripción, visibilidad pública/privada y un identificador UUID único para compartir por URL.
  - Los catálogos están asociados a usuarios registrados.

- **Organización de Contenido**
  - Cada catálogo puede contener múltiples álbumes.
  - Cada álbum puede contener múltiples fotos.
  - Las fotos almacenan un título, fecha de carga y una URL de imagen (pensado para integración con Cloudinary u otros servicios externos).

- **Sistema de Usuarios**
  - Se utiliza el sistema de autenticación de Django.
  - Los catálogos están relacionados con los usuarios, pero no se ha implementado frontend ni endpoints para registro o login.

- **Compartición**
  - Los catálogos pueden ser públicos (accesibles por UUID) o privados (solo el dueño puede verlos).
  - La lógica de visibilidad y permisos está implementada en la capa de servicios.

- **Estructura del proyecto**
  - Modelos (`models.py`): Definen la estructura de datos y relaciones.
  - Repositorios (`catalog_repositories.py`): Encapsulan el acceso a la base de datos.
  - Servicios (`catalog_services.py`): Implementan la lógica de negocio y reglas de visibilidad.

---

## Funcionalidades pendientes / No implementadas

- **Frontend**
  - No hay vistas, formularios, templates ni endpoints web.
  - No existe una interfaz gráfica para usuarios finales.

- **API REST**
  - No se han creado endpoints para interactuar con los modelos desde aplicaciones externas.

- **Registro y login de usuarios vía web**
  - Solo es posible crear usuarios desde la shell de Django o el admin.

- **Carga de imágenes**
  - Las fotos solo almacenan la URL; no hay integración directa con servicios de almacenamiento ni formularios de subida.

- **Panel de usuario y gestión de contenido desde la web**
  - No implementado.

---

## ¿Cómo interactuar con el proyecto actualmente?

- **Crear usuarios desde la shell de Django:**
  ```python
  from django.contrib.auth.models import User
  User.objects.create_user(username='usuario', password='contraseña')
  ```

- **Crear catálogos usando la capa de servicios:**
  ```python
  from django.contrib.auth.models import User
  from catalogs.catalog_services import CatalogService

  user = User.objects.get(username='usuario')
  catalog = CatalogService.create_catalog(
      owner=user,
      title="Mi primer catálogo",
      description="Catálogo de prueba para la universidad",
      is_public=True
  )
  ```

- **Crear álbumes y fotos (ejemplo):**
  ```python
  from catalogs.catalog_services import AlbumService, PhotoService

  album = AlbumService.create_album(
      catalog=catalog,
      title="Vacaciones",
      description="Fotos de vacaciones"
  )

  photo = PhotoService.add_photo_to_album(
      album=album,
      title="En la playa",
      image_url="https://url-de-la-foto.jpg"
  )
  ```

---

## Requisitos

- Python 3.x
- Django 4.x
- MySQL
- PyMySQL (como cliente de base de datos)

---

## Estado del proyecto

> El backend y la lógica de negocio están implementados y probados con MySQL.  
> Falta desarrollar la interfaz de usuario (web o API) para interacción directa por parte de los usuarios finales.
