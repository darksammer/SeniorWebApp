from django.shortcuts import render,render_to_response
from chartit import DataPool, Chart
from .models import Financial_Ratio

# Create your views here.
def chart_view(request):
    data = \
        DataPool(series=
            [{'options': {
                'source': Financial_Ratio.objects.all()},
                'terms': [
                    'year','eps','beta']}
            ])

    cht = Chart(
        datasource = data,
        series_options = 
        [{'options':{
                'type': 'line',
                'stacking': False},
            'terms':{
                'year':['eps','beta']
                }}],
        chart_options =
         {'title': {
             'text': 'sample chart'},
        'xAxis': {
            'title': {
                'text': 'time'}}})

    return render_to_response('valuation/chart.html', {'chart': cht})
