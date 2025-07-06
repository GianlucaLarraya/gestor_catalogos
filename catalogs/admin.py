from django.contrib import admin

from .models import Catalog, Album, Photo

admin.site.register(Catalog)
admin.site.register(Album)
admin.site.register(Photo)
