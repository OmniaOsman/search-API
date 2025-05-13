from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .service import *
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status


class ProductListView(APIView):
    @extend_schema(
        summary="Add a new product",
        description="Add a new product to the database.",
        tags=["Products"],
        request=AddProductSerializer,
        responses={
            201: "product added successfully",
        }
    )
    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_product(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer

    @extend_schema(
        summary="Search products",
        description="Search products by name.",
        tags=["Products"],
        parameters=[SearchProductSerializer],
        responses={
            200: ProductSerializer(many=True),
        }
    )
    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if not query:
            return Product.objects.none()
        return search_products(query)
