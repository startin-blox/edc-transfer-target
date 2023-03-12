from django.contrib import admin
from .models import StoredFile

class StoredFileAdmin(admin.ModelAdmin):
    fields = ['original_filename', 'path', 'url']

admin.site.register(StoredFile, StoredFileAdmin)