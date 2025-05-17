from unicodedata import category, normalize
from functools import reduce
from django.db.models import F, Q, Func, TextField, Count, Case, When, IntegerField
from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
import hashlib
from products.models import Product


def add_product(data: dict) -> dict:
    Product.objects.create(**data)
    return {
        "success": True,
        "message": "Product added successfully.",
    }


class UnaccentImmutable(Func):
    function = 'unaccent_immutable'
    output_field = TextField()


def remove_accents(text: str) -> str:
    return ''.join(c for c in normalize('NFD', text) if category(c) != 'Mn')


def normalize_query(query: str) -> tuple[str, str, set[str]]:
    query_unaccented = remove_accents(query)
    tokens = set(query.lower().split() + query_unaccented.lower().split())
    return query.strip(), query_unaccented, tokens


def search_products(validated_data: dict) -> list[Product]:
    query = validated_data.get('query', '').strip()
    page = validated_data.get('page', 1)
    category_id = validated_data.get('category_id')
    brand_id = validated_data.get('brand_id')

    if not query:
        return Product.objects.none()

    query, query_unaccented, tokens = normalize_query(query)

    cache_key = f"search_products:{hashlib.md5(f'{query}:{page}:{category_id}:{brand_id}'.encode()).hexdigest()}"
    cached_ids = cache.get(cache_key)
    if cached_ids is not None:
        preserved_order = {id: i for i, id in enumerate(cached_ids)}
        qs = Product.objects.filter(id__in=cached_ids)
        return sorted(qs, key=lambda p: preserved_order.get(p.id, 0))

    SEARCH_FIELDS = [
        'name_en', 'name_ar',
        'brand__name_en', 'brand__name_ar',
        'category__name_en', 'category__name_ar',
    ]

    filters = Q()
    if category_id:
        filters &= Q(category_id=category_id)
    if brand_id:
        filters &= Q(brand_id=brand_id)

    qs = Product.objects.filter(filters)

    partial_q = Q()
    for field in SEARCH_FIELDS:
        partial_q |= Q(**{f"{field}__icontains": query}) | Q(**{f"{field}__icontains": query_unaccented})

    token_q = Q()
    for token in tokens:
        for field in SEARCH_FIELDS:
            token_q |= Q(**{f"{field}__icontains": token})

    trigram_sim = (
        TrigramSimilarity(UnaccentImmutable(F('name_en')), query_unaccented.lower()) * 2 +
        TrigramSimilarity(UnaccentImmutable(F('name_ar')), query_unaccented.lower()) * 2 +
        TrigramSimilarity(UnaccentImmutable(F('brand__name_en')), query_unaccented.lower()) +
        TrigramSimilarity(UnaccentImmutable(F('brand__name_ar')), query_unaccented.lower())
    )

    qs = qs.annotate(similarity=trigram_sim).filter(
        Q(similarity__gt=0.1) | partial_q | token_q
    )

    full_token_match_cond = reduce(lambda q, t: q & Q(name_en__icontains=t), tokens, Q())

    qs = qs.annotate(
        full_token_match=Case(
            When(full_token_match_cond, then=1),
            default=0,
            output_field=IntegerField()
        ),
        token_match_count=Count(
            Case(
                *[When(**{f"{field}__icontains": token}, then=1)
                  for token in tokens for field in SEARCH_FIELDS],
                output_field=IntegerField()
            )
        ),
        priority=F('similarity') * 2 + F('token_match_count') + F('full_token_match') * 3
    ).order_by('-priority', '-similarity', '-token_match_count')

    page_size = 20
    start = page_size * (page - 1)
    end = start + page_size
    paged = list(qs.only('id', 'name_ar', 'name_en')[start:end])

    cache.set(cache_key, [p.id for p in paged], 300)
    return paged