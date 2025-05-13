from rest_framework import serializers
from .models import Product
from core.utils import ResponseSerializer


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'name_en', 'name_ar']


class ProductResponseSerializer(ResponseSerializer):
    payload = ProductSerializer(many=True)


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name_en', 'name_ar', 'brand', 'category', 'nutrition_facts']

    def validate_name_en(self, value):
        if Product.objects.filter(name_en=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value


class SearchProductSerializer(serializers.Serializer):
    query = serializers.CharField()
