from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .service import *
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination


class ProductListView(APIView):
    @extend_schema(
        summary="Add a new product",
        description="Add a new product to the database.",
        tags=["Products"],
        request=AddProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_product(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)


class SearchAnonRateThrottle(AnonRateThrottle):
    scope = 'search_anon'


class ProductSearchView(GenericAPIView):
    serializer_class = SearchProductSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [SearchAnonRateThrottle]

    @extend_schema(
        summary="Advanced product search",
        description="Search products by name, brand, or category with support for partial keywords, misspellings, and mixed languages (English/Arabic).",
        tags=["Products"],
        parameters=[SearchProductSerializer],
        request=SearchProductSerializer,
        responses={
            200: ProductSerializer(many=True),
        }
    )

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        products = search_products(serializer.validated_data)
        page = self.paginate_queryset(products)
        serializer = ProductSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
        