from django.shortcuts import render,render_to_response
from chartit import DataPool, Chart
from .models import *

# Create your views here.
def chart_view(request, name):
    data = \
        DataPool(series=
            [{'options': {
                'source': Fair_Value.objects.filter(short_name = name)},
                'terms': [
                    'year','price','fair','short_name']}
            ])

    cht = Chart(
        datasource = data,
        series_options = 
        [{'options':{
                'type': 'area',
                'stacking': False,
                'fillOpacity': 0.1,
                'color': '#5b9aff',
                },
            'terms':{
                'year':['price'],
                }},
         {'options':{
                'type': 'line',
                'stacking' : False,
                'dashStyle' : 'longdash',
                'color': '#000000'},
            'terms':{
                'year':['fair']
         }}],
        chart_options =
         {'title': {
             'text': 'sample chart'},
        'xAxis': {
            'title': {
                'text': 'time'}}})

    return render_to_response('valuation/chart.html', {'chart': cht})
