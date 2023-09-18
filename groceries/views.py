from typing import List
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@permission_classes([IsAuthenticated])
class CategoryList(APIView):
    def get(self, request: HttpRequest) -> HttpResponse:
        categories = Category.objects
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class ProductList(APIView):
    def get(self, request: HttpRequest) -> HttpResponse:
        user_id = request.user.id
        products = Product.objects.filter(user_id=user_id).order_by('category')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> HttpResponse:
        user_id = request.user.id

        try:
            Product.objects.get(name=request.data['name'].capitalize())
            return Response("Product with this name already exists")
        except Product.DoesNotExist:
            pass 

        serializer = ProductSerializer(data=request.data)
        name = request.data['name'].capitalize()

        if serializer.is_valid():
            serializer.validated_data['name'] = name
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ProductDetails(APIView):
    def get(self, request: HttpRequest, pk) -> HttpResponse:
        user_id = request.user.id

        try:
            product = Product.objects.filter(user_id=user_id).get(id=pk)
            serializer = ProductSerializer(product)

            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request: HttpRequest, pk) -> HttpResponse:
        user_id = request.user.id

        try:
            product = Product.objects.filter(user_id=user_id).get(id=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

