from django.conf.urls import url
from . import views

app_name = 'covidVisualizer'

urlpatterns = [
    url('home/', views.visualization_list, name='list'),
     url('confirmedplot/', views.confirmedPlot, name='confirmedplot'),
    url('deceasedplot/', views.deceasedPlot, name='deceasedPlot'),
    url('recoveredplot/', views.recoveredPlot, name='recoveredPlot'),
    url('testedplot/', views.testedPlot, name='testedPlot')
]