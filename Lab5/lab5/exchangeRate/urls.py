from django.urls import path

from . import views

app_name = 'exchangeRate'
urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
