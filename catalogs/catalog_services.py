from .catalog_repositories import CatalogRepository, AlbumRepository, PhotoRepository
from .models import Catalog, Album, Photo
from django.contrib.auth import get_user_model
from typing import Optional, List

User = get_user_model()

class CatalogService:
    @staticmethod
    def create_catalog(owner: User, title: str, description: str = '', is_public: bool = False) -> Catalog:
        return CatalogRepository.create(owner, title, description, is_public)

    @staticmethod
    def get_catalog_for_user(catalog_id: int, user: User) -> Optional[Catalog]:
        catalog = CatalogRepository.get_by_id(catalog_id)
        if catalog and catalog.owner == user:
            return catalog
        return None

    @staticmethod
    def get_catalog_by_uuid(uuid, user: Optional[User] = None) -> Optional[Catalog]:
        catalog = CatalogRepository.get_by_uuid(uuid)
        if catalog:
            if catalog.is_public or (user and catalog.owner == user):
                return catalog
        return None

    @staticmethod
    def list_user_catalogs(user: User) -> List[Catalog]:
        return list(CatalogRepository.get_by_owner(user))

    @staticmethod
    def delete_catalog(catalog: Catalog, user: User) -> bool:
        if catalog.owner == user:
            CatalogRepository.delete(catalog)
            return True
        return False

class AlbumService:
    @staticmethod
    def create_album(catalog: Catalog, title: str, user: User) -> Optional[Album]:
        if catalog.owner == user:
            return AlbumRepository.create(catalog, title)
        return None

    @staticmethod
    def list_albums(catalog: Catalog, user: User) -> List[Album]:
        if catalog.is_public or catalog.owner == user:
            return list(AlbumRepository.get_by_catalog(catalog))
        return []

    @staticmethod
    def delete_album(album: Album, user: User) -> bool:
        if album.catalog.owner == user:
            AlbumRepository.delete(album)
            return True
        return False

class PhotoService:
    @staticmethod
    def add_photo(album: Album, title: str, image_url: str, user: User) -> Optional[Photo]:
        if album.catalog.owner == user:
            return PhotoRepository.create(album, title, image_url)
        return None

    @staticmethod
    def list_photos(album: Album, user: User) -> List[Photo]:
        if album.catalog.is_public or album.catalog.owner == user:
            return list(PhotoRepository.get_by_album(album))
        return []

    @staticmethod
    def delete_photo(photo: Photo, user: User) -> bool:
        if photo.album.catalog.owner == user:
            PhotoRepository.delete(photo)
            return True
        return False 