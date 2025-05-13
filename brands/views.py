from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from brands.serializers import BrandResponseSerializer, AddBulkBrandSerializer
from brands.service import *
from drf_spectacular.utils import extend_schema


class BrandListView(APIView):
    @extend_schema(
        summary="Get all brands",
        description="Retrieve all brands from the database.",
        tags=["Brands"],
        responses={ 200: BrandResponseSerializer(many=True), }
    )
    def get(self, request):
        response = get_all_brands()
        response = BrandResponseSerializer(data=response)
        response.is_valid(raise_exception=True)
        return Response(response.validated_data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Add a new brand",
        description="Add a new brand to the database.",
        tags=["Brands"],
        request=AddBulkBrandSerializer,
        responses={
            201: 'brands added successfully',
        },
    )
    def post(self, request):
        serializer = AddBulkBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_bulk_brands(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)
    