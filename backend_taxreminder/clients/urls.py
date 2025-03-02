# accounts/urls.py
from django.urls import path
from .views import  ClientCreateView,ClientDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('clients/', ClientCreateView.as_view(), name='client_create_get'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_details'),

]
