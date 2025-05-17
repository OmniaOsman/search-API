from django.db import models


class Brand(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="English Name", db_index=True)
    name_ar = models.CharField(max_length=255, verbose_name="Arabic Name")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name_en


