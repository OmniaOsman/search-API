from django.db import models
from categories.models import Category
from brands.models import Brand
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify


class Product(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="English Name", db_index=True)
    name_ar = models.CharField(max_length=255, verbose_name="Arabic Name")
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            GinIndex(fields=["name_en"], name="product_name_en_trgm_idx", opclasses=["gin_trgm_ops"]),
            GinIndex(fields=["name_ar"], name="product_name_ar_trgm_idx", opclasses=["gin_trgm_ops"]),
        ]

    def save(self, *args, **kwargs):
        """
        Update the search_vector field for full-text search before saving the object.
        Concatenate the English and Arabic product names to create a composite search vector.
        """
        from django.contrib.postgres.search import SearchVector
        
        # Update search_vector with combined English and Arabic product names
        self.search_vector = (
            SearchVector("name_en") + SearchVector("name_ar")
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_en} - {self.brand.name_en}"
