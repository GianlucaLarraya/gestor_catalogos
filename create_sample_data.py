#!/usr/bin/env python
"""
Script para crear datos de ejemplo para la aplicación Cataly
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cataly.settings')
django.setup()

# Importar después de configurar Django
from django.contrib.auth.models import User
from catalogs.models import Catalog, Album, Photo

def create_sample_data():
    print("Creando datos de ejemplo para Cataly...")
    
    # Crear usuario de ejemplo
    user, created = User.objects.get_or_create(
        username='demo_user',
        defaults={
            'email': 'demo@example.com',
            'first_name': 'Demo',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('demo123')
        user.save()
        print(f"Usuario creado: {user.username}")
    else:
        print(f"Usuario existente: {user.username}")
    
    # Crear catálogos de ejemplo
    catalogs_data = [
        {
            'title': 'Fotografía de Naturaleza',
            'description': 'Una colección de hermosas fotografías de paisajes naturales, flora y fauna salvaje.',
            'is_public': True,
            'albums': [
                {
                    'title': 'Paisajes Montañosos',
                    'photos': [
                        {'title': 'Montañas Nevadas', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'},
                        {'title': 'Valle Verde', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'},
                        {'title': 'Cascada Cristalina', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'},
                    ]
                },
                {
                    'title': 'Flora Silvestre',
                    'photos': [
                        {'title': 'Flores de Primavera', 'image_url': 'https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=800'},
                        {'title': 'Árboles Centenarios', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'},
                    ]
                }
            ]
        },
        {
            'title': 'Arte Urbano',
            'description': 'Explorando el arte callejero y la creatividad en las ciudades del mundo.',
            'is_public': True,
            'albums': [
                {
                    'title': 'Grafitis Coloridos',
                    'photos': [
                        {'title': 'Mural Callejero', 'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800'},
                        {'title': 'Arte Abstracto', 'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800'},
                    ]
                }
            ]
        },
        {
            'title': 'Viajes por el Mundo',
            'description': 'Recuerdos de viajes increíbles alrededor del mundo.',
            'is_public': True,
            'albums': [
                {
                    'title': 'Europa',
                    'photos': [
                        {'title': 'Torre Eiffel', 'image_url': 'https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=800'},
                        {'title': 'Coliseo Romano', 'image_url': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800'},
                        {'title': 'Puente de Londres', 'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800'},
                    ]
                },
                {
                    'title': 'Asia',
                    'photos': [
                        {'title': 'Templo de Kyoto', 'image_url': 'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=800'},
                        {'title': 'Gran Muralla', 'image_url': 'https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800'},
                    ]
                }
            ]
        },
        {
            'title': 'Mi Colección Privada',
            'description': 'Una colección personal de fotografías privadas.',
            'is_public': False,
            'albums': [
                {
                    'title': 'Fotos Familiares',
                    'photos': [
                        {'title': 'Cumpleaños', 'image_url': 'https://images.unsplash.com/photo-1464349153735-7db50ed83c84?w=800'},
                        {'title': 'Vacaciones', 'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'},
                    ]
                }
            ]
        }
    ]
    
    for catalog_data in catalogs_data:
        catalog, created = Catalog.objects.get_or_create(
            title=catalog_data['title'],
            owner=user,
            defaults={
                'description': catalog_data['description'],
                'is_public': catalog_data['is_public']
            }
        )
        
        if created:
            print(f"Catálogo creado: {catalog.title}")
        else:
            print(f"Catálogo existente: {catalog.title}")
        
        # Crear álbumes para este catálogo
        for album_data in catalog_data['albums']:
            album, created = Album.objects.get_or_create(
                title=album_data['title'],
                catalog=catalog,
                defaults={}
            )
            
            if created:
                print(f"  - Álbum creado: {album.title}")
            else:
                print(f"  - Álbum existente: {album.title}")
            
            # Crear fotos para este álbum
            for photo_data in album_data['photos']:
                photo, created = Photo.objects.get_or_create(
                    title=photo_data['title'],
                    album=album,
                    defaults={
                        'image_url': photo_data['image_url']
                    }
                )
                
                if created:
                    print(f"    - Foto creada: {photo.title}")
                else:
                    print(f"    - Foto existente: {photo.title}")
    
    print("\n¡Datos de ejemplo creados exitosamente!")
    print(f"Usuario: {user.username} (contraseña: demo123)")
    print("Puedes iniciar sesión en el admin para gestionar los datos.")

if __name__ == '__main__':
    create_sample_data() 