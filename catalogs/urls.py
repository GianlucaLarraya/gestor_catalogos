from django.urls import path
from . import views

app_name = 'catalogs'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('my-catalogs/', views.my_catalogs, name='my_catalogs'),
    path('my-catalogs/create/', views.catalog_create, name='catalog_create'),
    path('my-catalogs/<uuid:catalog_uuid>/edit/', views.catalog_update, name='catalog_update'),
    path('my-catalogs/<uuid:catalog_uuid>/delete/', views.catalog_delete, name='catalog_delete'),
    path('catalog/<uuid:catalog_uuid>/album/create/', views.album_create, name='album_create'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/edit/', views.album_update, name='album_update'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/delete/', views.album_delete, name='album_delete'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/photo/create/', views.photo_create, name='photo_create'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/photo/<int:photo_id>/edit/', views.photo_update, name='photo_update'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/photo/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
    path('search/', views.search, name='search'),
    path('catalog/<uuid:catalog_uuid>/', views.catalog_detail, name='catalog_detail'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('catalog/<uuid:catalog_uuid>/album/<int:album_id>/photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
] 