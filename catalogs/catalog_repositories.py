from .models import Catalog, Album, Photo
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional

User = get_user_model()

class CatalogRepository:
    @staticmethod
    def get_by_id(catalog_id: int) -> Optional[Catalog]:
        return Catalog.objects.filter(id=catalog_id).first()

    @staticmethod
    def get_by_uuid(uuid) -> Optional[Catalog]:
        return Catalog.objects.filter(uuid=uuid).first()

    @staticmethod
    def get_by_owner(user: User) -> QuerySet:
        return Catalog.objects.filter(owner=user)

    @staticmethod
    def get_public_by_uuid(uuid) -> Optional[Catalog]:
        return Catalog.objects.filter(uuid=uuid, is_public=True).first()

    @staticmethod
    def create(owner: User, title: str, description: str = '', is_public: bool = False) -> Catalog:
        return Catalog.objects.create(owner=owner, title=title, description=description, is_public=is_public)

    @staticmethod
    def delete(catalog: Catalog):
        catalog.delete()

class AlbumRepository:
    @staticmethod
    def get_by_id(album_id: int) -> Optional[Album]:
        return Album.objects.filter(id=album_id).first()

    @staticmethod
    def get_by_catalog(catalog: Catalog) -> QuerySet:
        return Album.objects.filter(catalog=catalog)

    @staticmethod
    def create(catalog: Catalog, title: str) -> Album:
        return Album.objects.create(catalog=catalog, title=title)

    @staticmethod
    def delete(album: Album):
        album.delete()

class PhotoRepository:
    @staticmethod
    def get_by_id(photo_id: int) -> Optional[Photo]:
        return Photo.objects.filter(id=photo_id).first()

    @staticmethod
    def get_by_album(album: Album) -> QuerySet:
        return Photo.objects.filter(album=album)

    @staticmethod
    def create(album: Album, title: str, image_url: str) -> Photo:
        return Photo.objects.create(album=album, title=title, image_url=image_url)

    @staticmethod
    def delete(photo: Photo):
        photo.delete() 