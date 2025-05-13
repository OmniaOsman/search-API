from products.models import Product
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from django.db.models.functions import Greatest
from .utils import normalize_text

def add_product(data):
    Product.objects.create(**data)
    return {
        "success": True,
        "message": "Product added successfully.",
    }

def search_products(query, limit=20):
    # Normalize query
    norm_query = normalize_text(query)
    if not norm_query:
        return Product.objects.none()
    # Split query into words for partial/mixed-language support
    query_words = norm_query.split()

    # Prepare full-text search vectors for both languages
    vector = (
        SearchVector('name_en', weight='A', config='english') +
        SearchVector('name_ar', weight='A', config='arabic')
    )
    search_query_en = SearchQuery(query, config='english')
    search_query_ar = SearchQuery(query, config='arabic')

    # Trigram similarity for fuzzy search
    trigram_en = TrigramSimilarity('name_en', query)
    trigram_ar = TrigramSimilarity('name_ar', query)

    # Full-text and trigram search
    qs1 = Product.objects.annotate(
        rank=SearchRank(vector, search_query_en) + SearchRank(vector, search_query_ar),
        trigram=Greatest(trigram_en, trigram_ar)
    ).filter(
        Q(rank__gte=0.1) | Q(trigram__gte=0.2)
    )

    # icontains for partials and mixed
    icontains_filter = Q()
    for word in query_words:
        icontains_filter |= Q(name_en__icontains=word) | Q(name_ar__icontains=word)
    qs2 = Product.objects.filter(icontains_filter)

    # Union and deduplicate (by id)
    all_ids = set(list(qs1.values_list('id', flat=True)) + list(qs2.values_list('id', flat=True)))
    products = Product.objects.filter(id__in=all_ids)

    # Optional: sort by rank/trigram if present, fallback to id
    products = products.annotate(
        rank=SearchRank(vector, search_query_en) + SearchRank(vector, search_query_ar),
        trigram=Greatest(trigram_en, trigram_ar)
    ).order_by('-rank', '-trigram', 'id')[:limit]

    return products
