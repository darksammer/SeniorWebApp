from django.shortcuts import render,render_to_response, redirect
from django.http import Http404
from django.db.models import F, Prefetch, Max
from chartit import DataPool, Chart
from .models import *
from django.utils import timezone
import decimal

# Create your views here.
def index_view(request):
    fund_list = Dividend_Yield.objects.raw('select id, short_name_id, max(period_id), div_yield\
                                            from valuation_dividend_yield\
                                            group by short_name_id\
                                            order by period_id desc, div_yield desc\
                                            limit 5')

    return render(request,'valuation/Home.html', {'fund_list':fund_list})

def search_view(request):
    search_string = request.GET.get('q')
    if search_string == "":
        raise Http404("Fund not found")
    else:
        return redirect(fund_view, name=search_string)

def fund_view(request,name):

    try:
        fund_data = General_Information.objects.get(short_name = name)
        chart_data = Fair_Value.objects.filter(short_name = name).select_related().order_by('-period')
    except:
        raise Http404('Fund not found')

    #fund age
    age = timezone.now().year - fund_data.ipo_date

    #chart parameter
    data = \
        DataPool(series=
            [{'options': {
                'source': chart_data},
                'terms': [
                    'period','price','fair','short_name']}
            ])

    value_chart = Chart(
        datasource = data,
        series_options = 
        [{'options':{
                'type': 'area',
                'stacking': False,
                'fillOpacity': 0.1,
                'color': '#5b9aff',
                },
            'terms':{
                'period':['price'],
                }},
         {'options':{
                'type': 'line',
                'stacking' : False,
                'dashStyle' : 'longdash',
                'color': '#000000'},
            'terms':{
                'period':['fair']
         }}],
        chart_options =
         {'title': {
            'text': 'Fair Price'},
            'xAxis': {
                'type': 'datetime',
                'title': {'text': 'time'}},
            'yAxis':{
                'title': {'text': 'Price'}},
            
        })

    
    return render(request,'valuation/fund.html',{'name': name, 'age':age, 'fund_data':fund_data,
                                                    'chart':value_chart, 'chart_data':chart_data, 'age':age})

def ranking_view(request,rank_type):
    #ranking by latest_yield
    if rank_type == "yield":
        fund_list = Dividend_Yield.objects.raw('select id, short_name_id, max(period_id), div_yield\
                                            from valuation_dividend_yield\
                                            group by short_name_id\
                                            order by period_id desc, div_yield desc')
        return render(request, 'valuation/ranking.html' , {'fund_list':fund_list, 'rank_type':rank_type})

def test_page(request):
    chart_data = Fair_Value.objects.filter(short_name = 'test').select_related().order_by('-period')
    return render(request, 'valuation/test_page.html' , {'chart_data':chart_data})