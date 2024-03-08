from django.urls import path
from . import views


# urlconf
urlpatterns = [
    path('normchart/<str:pk>/', views.normchart, name='normchart'),
    path('candle/<str:pk>/', views.candle, name='candle'),
    path('tinkerSetter/<str:pk>/', views.tinkerSetter, name='tinkerSetter')
]
