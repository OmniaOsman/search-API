from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify
from categories.models import Category
from django.contrib.postgres.search import SearchVectorField
from brands.models import Brand


class Product(models.Model):
    name_en = models.CharField(max_length=255, verbose_name="English Name")
    name_ar = models.CharField(max_length=255, verbose_name="Arabic Name")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    nutrition_facts = models.JSONField(blank=True, null=True)
    search_vector = SearchVectorField(blank=True, null=True, editable=False)

    class Meta:
        indexes = [
            GinIndex(
                fields=['search_vector'],
                name='search_vector_gin_idx'
            ),
            GinIndex(
                fields=['name_ar'],
                name='name_ar_gin_idx',
                opclasses=['gin_trgm_ops']
            ),
            GinIndex(
                fields=['name_en'],
                name='name_en_gin_idx',
                opclasses=['gin_trgm_ops']
            ),
        ]

