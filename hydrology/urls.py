from django.urls import path

from hydrology import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gis_upload', views.gis_upload, name='gis_upload'),
    path('gis_results', views.gis_results, name='gis_results'),
    path('instructions', views.instructions, name= 'instructions'),
    path('download_csv', views.download_csv, name = 'download_csv'),
    path('download_shp', views.download_shp, name = 'download_shp'),
]