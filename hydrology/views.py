from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
import numpy as np
import pandas as pd
import geopandas as gpd
import os
from geopandas import datasets, GeoDataFrame, read_file, overlay
from hydrology.functions import zip_to_df
from hydrology.DataFrameFunctions import overlay_hydrology, create_overall_map
from django.utils.encoding import smart_str
import zipfile
from wsgiref.util import FileWrapper

def index(request):
    return render(request, 'index.html')

def gis_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            soils = form.cleaned_data['soils']
            delineationdf = zip_to_df(request.FILES['delineation_file'])
            imperviousdf = zip_to_df(request.FILES['coverage_file'])
            table = overlay_hydrology(delineationdf, imperviousdf, soils)
            overall_map = create_overall_map(delineationdf, imperviousdf)
            
            return render(request, 'gis_results.html', {'table': table.to_html()})
        
    else:
        form = UploadFileForm()
    return render(request, 'file_upload_form.html', {'form': form})

def gis_results(request):
    return render(request, 'gis_results.html')

def instructions(request):
    return render(request, 'instructions.html')

def download_csv(request):
    file_path = 'hydrology/output/Drainage_Areas.csv'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
        
def download_shp(request):
    zf = zipfile.ZipFile('hydrology/output/drainage_area_shp.zip', mode = 'w')
    zf.write('hydrology/output/Drainage_Areas.cpg')
    zf.write('hydrology/output/Drainage_Areas.dbf')
    zf.write('hydrology/output/Drainage_Areas.shp')
    zf.write('hydrology/output/Drainage_Areas.shx')
    
    file_path = 'hydrology/output/drainage_area_shp.zip'
    wrapper = FileWrapper(file_path)
    if os.path.exists(file_path):
            response = HttpResponse(wrapper, content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response