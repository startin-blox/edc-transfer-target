from django.db import models



class StoredFile(models.Model):
    original_filename = models.CharField(max_length=2048)
    url = models.URLField()
    path = models.CharField(max_length=2048)

    def __str__(self):
        return self.original_filename