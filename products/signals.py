from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from products.models import Product


@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    # Recalculate the search vector combining product, brand, category fields
    vector = (
        SearchVector('name_en', weight='A') +
        SearchVector('name_ar', weight='A') +
        SearchVector('brand__name_en', weight='B') +
        SearchVector('category__name_en', weight='B')
    )
    # Use update() on queryset to avoid recursion, update only this instance
    Product.objects.filter(pk=instance.pk).update(search_vector=vector)
