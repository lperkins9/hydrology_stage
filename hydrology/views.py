from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import numpy as np
import pandas as pd
import geopandas as gpd
from geopandas import datasets, GeoDataFrame, read_file, overlay
from hydrology.functions import zip_to_df
from hydrology.DataFrameFunctions import overlay_hydrology


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
            
            return render(request, 'gis_results.html', {'table': table.to_html()})
        
    else:
        form = UploadFileForm()
    return render(request, 'file_upload_form.html', {'form': form})

def gis_results(request):
    return render(request, 'gis_results.html')

def instructions(request):
    return render(request, 'instructions.html')