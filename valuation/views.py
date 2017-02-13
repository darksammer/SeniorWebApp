from django.shortcuts import render,render_to_response, redirect
from django.http import Http404
from django.db.models import F
from chartit import DataPool, Chart
from .models import *

# Create your views here.
def index_view(request):
    fund_list = Dividend_Yield.objects.raw('select valuation_dividend_yield.id, max(valuation_dividend_yield.period) as period, valuation_dividend_yield.div_yield,\
                                                valuation_dividend_yield.short_name_id , valuation_general_information.full_name from valuation_dividend_yield\
                                                join valuation_general_information on valuation_dividend_yield.short_name_id = valuation_general_information.short_name\
                                                group by short_name_id\
                                                order by div_yield DESC, period DESC\
                                                limit 5')
    
    best_fund = Fair_Value.objects.raw('select id, short_name_id, period, price, fair\
                                                    from valuation_fair_value\
                                                    where short_name_id = (select short_name_id from valuation_dividend_yield\
                                                                            order by div_yield DESC limit 1)\
                                                    group by short_name_id, period')

    data = \
        DataPool(series=
            [{'options': {
                'source': best_fund},
                'terms': [
                    'period','price','fair','short_name_id']}
            ])

    index_chart = Chart(
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
            'text': best_fund[0].short_name_id.upper()},
            'xAxis': {
                'type': 'datetime',
                'title': {'text': 'time'}},
            'yAxis':{
                'title': {'text': 'Price'}},
            
        })

    return render(request,'valuation/Home.html', {'fund_list':fund_list, 'chart':index_chart})

def search_view(request):
    search_string = request.GET.get('q')
    if search_string == "":
        raise Http404("Fund not found")
    else:
        return redirect(fund_view, name=search_string)

def fund_view(request,name):

    try:
        fund_data = General_Information.objects.get(short_name = name)
    except:
        raise Http404('Fund not found')

    data = \
        DataPool(series=
            [{'options': {
                'source': Fair_Value.objects.filter(short_name = name)},
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

    
    return render(request,'valuation/fund.html',{'name': name , 'fund_data':fund_data, 'chart':value_chart})

def ranking_view(request,rank_type):
    #ranking by latest_yield
    if rank_type == "yield":
        fund_list = Dividend_Yield.objects.raw('select valuation_dividend_yield.id, max(valuation_dividend_yield.period) as period, valuation_dividend_yield.div_yield,\
                                                valuation_dividend_yield.short_name_id , valuation_general_information.full_name from valuation_dividend_yield\
                                                join valuation_general_information on valuation_dividend_yield.short_name_id = valuation_general_information.short_name\
                                                group by short_name_id\
                                                order by div_yield DESC, period DESC')
        return render(request, 'valuation/ranking.html' , {'fund_list':fund_list, 'rank_type':rank_type})
    #ranking by price&fair
    elif rank_type == "fair":
        fund_list = Fair_Value.objects.raw('select valuation_fair_value.id , valuation_fair_value.short_name_id , valuation_general_information.full_name , valuation_fair_value.price - valuation_fair_value.fair as diff ,\
                                            max(valuation_fair_value.period) as period from valuation_fair_value\
                                            join valuation_general_information on valuation_fair_value.short_name_id = valuation_general_information.short_name\
                                            group by short_name_id\
                                            order by diff DESC, period')
        return render(request, 'valuation/ranking.html' , {'fund_list':fund_list, 'rank_type':rank_type})
    #anything else
    else:
        raise Http404("Page not found")