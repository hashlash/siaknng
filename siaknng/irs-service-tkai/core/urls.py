from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-matkul', views.getMatkul, name='get-matkul'),
    path('set-matkul', views.setMatkul, name='set-matkul')
]