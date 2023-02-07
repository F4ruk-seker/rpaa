from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(),name='mainQueryPage'),
    path('many-query/', views.ManyQuery.as_view(),name='manyQueryPage'),
]
