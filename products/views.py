from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.template import loader

from .models import Product
from .serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ProductPostIdSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # ---- Custom actions ----
    @action(detail=True, methods=['patch'], url_path='update-image')
    def update_image(self, request, pk=None):
        """PATCH /api/product/<id>/update-image/"""
        product = self.get_object()
        serializer = ProductImageSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], url_path='update-description')
    def update_description(self, request, pk=None):
        """PATCH /api/product/<id>/update-description/"""
        product = self.get_object()
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='update-post')
    def update_post_id(self, request, pk=None):
        """PATCH /api/product/<id>/update-post/"""
        product = self.get_object()        
        serializer = ProductPostIdSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Update status to True when post_id is updated
            product.status = True
            product.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get a product have status is False
    @action(detail=False, methods=['get'], url_path='pending-products')
    def pending_products(self, request):
        """GET /api/product/pending-products/"""
        pending_products = Product.objects.filter(status=False)
        serializer = self.get_serializer(pending_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---- HTML view riêng (không nằm trong ViewSet) ----
from django.views import View

class ProductHTMLView(View):
    def get(self, request):
        products = Product.objects.all()
        template = loader.get_template('product_form.html')
        return HttpResponse(template.render({'products': products}, request))

    def post(self, request):
        name = request.POST.get('name')
        price = request.POST.get('price')

        if name and price:
            Product.objects.create(
                name=name,
                price=int(price),
                description='',
                image='',
                post_id=''
            )
            return redirect('product')

        products = Product.objects.all()
        template = loader.get_template('product_form.html')
        context = {
            'error': 'Vui lòng điền đầy đủ thông tin',
            'products': products
        }
        return HttpResponse(template.render(context, request))

