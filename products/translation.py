from modeltranslation.translator import register, TranslationOptions
from .models import Product


@register('Product')
class ProductTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'es', 'fr')
    fallback_languages = {'default': ('en',)}
    localized_fields = ('translations',)
    fallback_fields = ('translations',)