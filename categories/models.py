from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify


class Category(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="English Name", db_index=True)
    name_ar = models.CharField(max_length=255, verbose_name="Arabic Name")
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            GinIndex(fields=["name_en"], name="category_name_en_trgm_idx", opclasses=["gin_trgm_ops"]),
            GinIndex(fields=["name_ar"], name="category_name_ar_trgm_idx", opclasses=["gin_trgm_ops"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_en
