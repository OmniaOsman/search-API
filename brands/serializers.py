from rest_framework import serializers
from django.core.exceptions import ValidationError
from core.utils import ResponseSerializer
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Brand
        fields = ['id', 'name_en', 'name_ar', 'slug']


class BrandResponseSerializer(ResponseSerializer):
    payload = BrandSerializer(many=True)


class AddBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name_en', 'name_ar']

    def validate_name_en(self, value):
        if Brand.objects.filter(name_en=value).exists():
            raise ValidationError("Brand with this name already exists.")
        return value
    

class AddBulkBrandSerializer(serializers.Serializer):
    brands = AddBrandSerializer(many=True, required=True)

    def validate_brands(self, value):
        if not value:
            raise ValidationError("At least one brand is required.")
        return value
