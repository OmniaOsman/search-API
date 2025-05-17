from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from categories.serializers import CategoryResponseSerializer, AddBulkCategorySerializer
from categories.service import *
from drf_spectacular.utils import extend_schema


class CategoryListView(APIView):
    @extend_schema(
        summary="Get all categories",
        description="Retrieve all categories from the database.",
        tags=["Categories"],
        responses={ 200: CategoryResponseSerializer(many=True), }           
    )
    def get(self, request):
        response = get_all_categories()
        response = CategoryResponseSerializer(data=response)
        response.is_valid(raise_exception=True)
        return Response(response.validated_data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Add a new category",
        description="Add a new category to the database.",
        tags=["Categories"],
        request=AddBulkCategorySerializer,
        responses={
            201: CategoryResponseSerializer(many=True),
            400: "Bad Request",
            500: "Internal Server Error"
        },
    )
    def post(self, request):
        serializer = AddBulkCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = add_bulk_category(serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)
