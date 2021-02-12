from django.shortcuts import render
from .models import visualize, visualizeDeceased, visualizeRecovered, visualizeTested

# Create your views here.
def visualization_list(request):
    return render(request, "covidVisualizer/visualizer_list.html")

def confirmedPlot(request):
    visualize()
    return render(request, 'confirmed_plot.html')

def deceasedPlot(request):
    visualizeDeceased()
    return render(request, 'deceased_plot.html')

def recoveredPlot(request):
    visualizeRecovered()
    return render(request, 'recovered_plot.html')

def testedPlot(request):
    visualizeTested()
    return render(request, 'tested_plot.html')