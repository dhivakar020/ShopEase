from django.urls import path
from .views import CategoryListCreateView, ProductListCreateView, ProductDetailView, ProductByCategoryView

urlpatterns = [
    path('getProduct/', ProductByCategoryView.as_view(), name='get_products_by_category'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateView.as_view(),name= 'product-list-create'),
    path('products/<int:pk>/',ProductDetailView.as_view(), name='product-detail',)
]