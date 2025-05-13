from .models import Brand
from django.utils.text import slugify


def get_all_brands():
    """
    Retrieve all brands from the database.
    """
    brands = Brand.objects.values('id', 'name_en', 'name_ar', 'slug')

    return {
        "success": True,
        "message": "Brands retrieved successfully",
        "payload": list(brands),
    }


def add_brand(brand):
    """
    Add a new brand to the database.
    """
    Brand.objects.create(
        name_en=brand['name_en'],
        name_ar=brand['name_ar']
    )
    return {
        "success": True,
        "message": "Brand added successfully",
    }


def add_bulk_brands(data):
    """
    Add multiple brands to the database in bulk.
    """
    brands_data = data.get('brands')
    existing_slugs = set(Brand.objects.values_list('slug', flat=True))
    seen_slugs = set()
    valid_brands = []
    for item in brands_data:
        name_en = item.get('name_en')
        slug = item.get('slug') or slugify(name_en)
        if not slug or slug in existing_slugs or slug in seen_slugs:
            continue  # skip duplicates or empty slugs
        seen_slugs.add(slug)
        valid_brands.append(Brand(name_en=name_en, name_ar=item.get('name_ar'), slug=slug))
    if valid_brands:
        Brand.objects.bulk_create(valid_brands)
    return {
        "success": True,
        "message": f"{len(valid_brands)} brands added successfully.",
    }
