from django.contrib import admin

# Register your models here.
from cloudapp.models import Image, Archive, Design


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ['id']
    list_display = ['name', 'file_size', 'get_size', 'user_id']
    list_filter = ['user_id']


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    exclude = ['id']
    list_display = ['name']
    list_filter = ['user_id']

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    exclude = ['id']
    list_display = ['title']