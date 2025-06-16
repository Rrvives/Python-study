from django.contrib import admin
from django.urls import path, include
from .views import TestView, JwtTestView, LoginView

urlpatterns = [
    # path('', include('car.urls')),
    path('a/', TestView.as_view(), name='test'),
    # 模拟token
    path('jwt/', JwtTestView.as_view(), name='JWT'),

    path('login/', LoginView.as_view(), name='login')
]