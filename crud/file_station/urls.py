from django.urls import path
from file_station import views


app_name = 'file_station'
urlpatterns = [
    path('<path:path>', views.File.as_view(), name='file'),
]
