from django.urls import path
from .views import MakeOrderView, GetOrderDetailsView

urlpatterns = [
    path('makeOrder/', MakeOrderView.as_view(), name='make_order'),
    path('getOrders/', GetOrderDetailsView.as_view(), name='get_orders'),
]
