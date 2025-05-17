from django.db import models


class Category(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="English Name", db_index=True)
    name_ar = models.CharField(max_length=255, verbose_name="Arabic Name")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name_en
