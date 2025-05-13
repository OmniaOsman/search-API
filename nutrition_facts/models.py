from django.db import models
from products.models import Product


class NutritionFact(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="nutrition")
    calories = models.PositiveIntegerField(default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sodium = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"Nutrition facts for {self.product.name_en}"

