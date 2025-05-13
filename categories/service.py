from categories.models import Category
from django.utils.text import slugify
from django.db.models import Q

def get_all_categories():
    """
    Retrieve all categories from the database.
    """
    categories = Category.objects.all().values('id', 'name_en', 'name_ar', 'slug')
    return {
        "success": True,
        "message": "Categories retrieved successfully",
        "payload": list(categories),
    }


def add_bulk_category(data):
    """
    Add a new category to the database.
    """
    categories_data = data.get('categories')
    # Get existing slugs from the database
    existing_slugs = set(Category.objects.values_list('slug', flat=True))
    seen_slugs = set()
    valid_categories = []
    for data in categories_data:
        name_en = data.get('name_en')
        slug = data.get('slug') or slugify(name_en)
        if not slug or slug in existing_slugs or slug in seen_slugs:
            continue  # skip duplicates or empty slugs
        seen_slugs.add(slug)
        valid_categories.append(Category(name_en=name_en, name_ar=data.get('name_ar'), slug=slug))
    
    return {
        "success": True,
        "message": f"{len(valid_categories)} categories added successfully.",
    }


