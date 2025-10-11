from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductHTMLView

router = DefaultRouter()
router.register(r'api/product', ProductViewSet, basename='product')

urlpatterns = [
    path('product/', ProductHTMLView.as_view(), name='product'),
]

urlpatterns += router.urls
