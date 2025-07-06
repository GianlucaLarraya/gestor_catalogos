from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Catalog, Album, Photo
from django import forms

def home(request):
    """Vista principal que muestra catálogos públicos"""
    public_catalogs = Catalog.objects.filter(is_public=True).order_by('-created_at')
    context = {
        'public_catalogs': public_catalogs,
        'total_catalogs': public_catalogs.count(),
    }
    return render(request, 'catalogs/home.html', context)

def user_login(request):
    """Vista para el login de usuarios"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('catalogs:home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'catalogs/login.html')

def user_register(request):
    """Vista para el registro de usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {user.username}.')
            return redirect('catalogs:home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = UserCreationForm()
    
    return render(request, 'catalogs/register.html', {'form': form})

def user_logout(request):
    """Vista para el logout de usuarios"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('catalogs:home')

@login_required
def my_catalogs(request):
    """Vista para mostrar los catálogos del usuario logueado"""
    from django.db.models import Count
    
    user_catalogs = Catalog.objects.filter(owner=request.user).order_by('-created_at')
    
    # Calcular estadísticas para cada catálogo de forma más eficiente
    for catalog in user_catalogs:
        catalog.album_count = catalog.albums.count()
        # Usar una consulta más eficiente para contar fotos
        catalog.photo_count = Photo.objects.filter(album__catalog=catalog).count()
    
    context = {
        'user_catalogs': user_catalogs,
        'total_catalogs': user_catalogs.count(),
    }
    return render(request, 'catalogs/my_catalogs.html', context)

def catalog_detail(request, catalog_uuid):
    """Vista para mostrar los detalles de un catálogo específico"""
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid)
    albums = catalog.albums.all().order_by('-created_at')
    
    # Verificar si el usuario puede ver este catálogo
    if not catalog.is_public and request.user != catalog.owner:
        return render(request, 'catalogs/access_denied.html')
    
    context = {
        'catalog': catalog,
        'albums': albums,
        'total_albums': albums.count(),
        'total_photos': sum(album.photos.count() for album in albums),
    }
    return render(request, 'catalogs/catalog_detail.html', context)

def album_detail(request, catalog_uuid, album_id):
    """Vista para mostrar los detalles de un álbum específico"""
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    photos = album.photos.all().order_by('-uploaded_at')
    
    # Verificar si el usuario puede ver este álbum
    if not catalog.is_public and request.user != catalog.owner:
        return render(request, 'catalogs/access_denied.html')
    
    context = {
        'catalog': catalog,
        'album': album,
        'photos': photos,
        'total_photos': photos.count(),
    }
    return render(request, 'catalogs/album_detail.html', context)

def photo_detail(request, catalog_uuid, album_id, photo_id):
    """Vista para mostrar los detalles de una foto específica"""
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    photo = get_object_or_404(Photo, id=photo_id, album=album)
    
    # Verificar si el usuario puede ver esta foto
    if not catalog.is_public and request.user != catalog.owner:
        return render(request, 'catalogs/access_denied.html')
    
    # Obtener fotos anterior y siguiente para navegación
    all_photos = list(album.photos.all().order_by('-uploaded_at'))
    current_index = None
    for i, p in enumerate(all_photos):
        if p.id == photo.id:
            current_index = i
            break
    
    prev_photo = all_photos[current_index + 1] if current_index is not None and current_index + 1 < len(all_photos) else None
    next_photo = all_photos[current_index - 1] if current_index is not None and current_index > 0 else None
    
    context = {
        'catalog': catalog,
        'album': album,
        'photo': photo,
        'prev_photo': prev_photo,
        'next_photo': next_photo,
    }
    return render(request, 'catalogs/photo_detail.html', context)

def search(request):
    """Vista para buscar catálogos públicos"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Catalog.objects.filter(
            is_public=True,
            title__icontains=query
        ).order_by('-created_at')
    
    context = {
        'query': query,
        'results': results,
        'total_results': len(results),
    }
    return render(request, 'catalogs/search.html', context)

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del catálogo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

@login_required
def catalog_create(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST)
        if form.is_valid():
            catalog = form.save(commit=False)
            catalog.owner = request.user
            catalog.save()
            messages.success(request, 'Catálogo creado exitosamente.')
            return redirect('catalogs:my_catalogs')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CatalogForm()
    return render(request, 'catalogs/catalog_form.html', {'form': form, 'action': 'Crear'})

@login_required
def catalog_update(request, catalog_uuid):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    if request.method == 'POST':
        form = CatalogForm(request.POST, instance=catalog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catálogo actualizado exitosamente.')
            return redirect('catalogs:my_catalogs')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CatalogForm(instance=catalog)
    return render(request, 'catalogs/catalog_form.html', {'form': form, 'action': 'Editar'})

@login_required
def catalog_delete(request, catalog_uuid):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    if request.method == 'POST':
        catalog.delete()
        messages.success(request, 'Catálogo eliminado exitosamente.')
        return redirect('catalogs:my_catalogs')
    return render(request, 'catalogs/catalog_confirm_delete.html', {'catalog': catalog})

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del álbum'}),
        }

@login_required
def album_create(request, catalog_uuid):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.catalog = catalog
            album.save()
            messages.success(request, 'Álbum creado exitosamente.')
            return redirect('catalogs:catalog_detail', catalog_uuid=catalog.uuid)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlbumForm()
    return render(request, 'catalogs/album_form.html', {'form': form, 'catalog': catalog, 'action': 'Crear'})

@login_required
def album_update(request, catalog_uuid, album_id):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Álbum actualizado exitosamente.')
            return redirect('catalogs:catalog_detail', catalog_uuid=catalog.uuid)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AlbumForm(instance=album)
    return render(request, 'catalogs/album_form.html', {'form': form, 'catalog': catalog, 'action': 'Editar'})

@login_required
def album_delete(request, catalog_uuid, album_id):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Álbum eliminado exitosamente.')
        return redirect('catalogs:catalog_detail', catalog_uuid=catalog.uuid)
    return render(request, 'catalogs/album_confirm_delete.html', {'album': album, 'catalog': catalog})

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la foto'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('La imagen es obligatoria.')
        return image

@login_required
def photo_create(request, catalog_uuid, album_id):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.save()
            messages.success(request, 'Foto subida exitosamente.')
            return redirect('catalogs:album_detail', catalog_uuid=catalog.uuid, album_id=album.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PhotoForm()
    return render(request, 'catalogs/photo_form.html', {'form': form, 'album': album, 'catalog': catalog, 'action': 'Crear'})

@login_required
def photo_update(request, catalog_uuid, album_id, photo_id):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    photo = get_object_or_404(Photo, id=photo_id, album=album)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto actualizada exitosamente.')
            return redirect('catalogs:album_detail', catalog_uuid=catalog.uuid, album_id=album.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'catalogs/photo_form.html', {'form': form, 'album': album, 'catalog': catalog, 'action': 'Editar'})

@login_required
def photo_delete(request, catalog_uuid, album_id, photo_id):
    catalog = get_object_or_404(Catalog, uuid=catalog_uuid, owner=request.user)
    album = get_object_or_404(Album, id=album_id, catalog=catalog)
    photo = get_object_or_404(Photo, id=photo_id, album=album)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Foto eliminada exitosamente.')
        return redirect('catalogs:album_detail', catalog_uuid=catalog.uuid, album_id=album.id)
    return render(request, 'catalogs/photo_confirm_delete.html', {'photo': photo, 'album': album, 'catalog': catalog})
