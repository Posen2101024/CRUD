from django.urls import path
from server import views


app_name = 'server'
urlpatterns = [
    path('ping', views.Ping.as_view(), name='ping'),
]
