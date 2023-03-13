from django.db import models



class StoredFile(models.Model):
    original_filename = models.CharField(max_length=2048, unique=True)
    url = models.URLField(unique=True)
    path = models.CharField(max_length=2048, unique=True)

    def __str__(self):
        return self.original_filename