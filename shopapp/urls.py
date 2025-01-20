from django.urls import path
from .views import (
    shop_index,
    group_list,
    GroupsListView,
    products_list,
    ProductListView,
    ProductDetailView,
    orders_list,
    OrderListView,
    OrderDetailView,
    create_product,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ShopIndexView,
)

app_name = "shopapp"

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('groups/',GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(),name='product_update'),
    path('products/<int:pk>/confirm-delete', ProductDeleteView.as_view(), name='product_delete'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details')

]
