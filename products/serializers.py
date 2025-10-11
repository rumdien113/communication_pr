from rest_framework import serializers
from .models import Product

# Serializer cho GET all (bỏ post_id)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['post_id']

class ProductPostIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['post_id']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image']