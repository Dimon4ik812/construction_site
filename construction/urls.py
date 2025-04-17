from django.urls import path

from construction import views
from construction.apps import ConstructionConfig
from construction.views import ServicesListView, send_order_to_telegram_2

app_name = ConstructionConfig.name

urlpatterns = [
    path('send-order-info/', send_order_to_telegram_2, name='send_order_to_telegram'),
    path('send-order/', views.send_order_to_telegram, name='send_order_to_telegram'),
    path("", ServicesListView.as_view(), name="home"),
]