from rest_framework import serializers
from .models import Category
from core.utils import ResponseSerializer


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_ar', 'slug']


class CategoryResponseSerializer(ResponseSerializer):
    payload = CategorySerializer(many=True)


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name_en', 'name_ar']

    def validate_name_en(self, value):
        if Category.objects.filter(name_en=value).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value


class AddBulkCategorySerializer(serializers.Serializer):
    categories = AddCategorySerializer(many=True, required=True)
