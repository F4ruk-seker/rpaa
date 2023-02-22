from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class MianPage(models.Model):
    banner_image = models.ImageField(upload_to='banner/')

    def get_banner(self):
        try:
            return self.banner_image.url
        except:
            pass

    def __str__(self):
        return 'Banner'

    def save(self, *args, **kwargs):
        import os

        from django.conf import settings

        directory = os.path.join(settings.MEDIA_ROOT, 'banner')
        for root, dirs, files in os.walk(directory):
            for file in files:
                os.remove(os.path.join(root, file))

        if not self.pk and MianPage.objects.count() > 0:
            raise ValidationError('Sadece bir resim yükleyiniz')
        super().save(*args, **kwargs)
