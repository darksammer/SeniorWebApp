from django.shortcuts import render,render_to_response, redirect
from django.http import Http404
from django.db.models import F, Prefetch, Max
from chartit import DataPool, Chart
from .models import *
from django.utils import timezone
import decimal

# Create your views here.
def index_view(request):
    fund_list = Dividend_Yield.objects.raw('select valuation_dividend_yield.id, valuation_dividend_yield.period_id, valuation_dividend_yield.div_yield,\
                                                valuation_dividend_yield.short_name_id\
                                                from valuation_dividend_yield\
                                                where valuation_dividend_yield.id in (\
                                                                    select max(valuation_dividend_yield.id)\
                                                                    from valuation_dividend_yield\
                                                                    group by valuation_dividend_yield.short_name_id\
                                                                )\
                                                order by valuation_dividend_yield.div_yield DESC\
                                                limit 5')

    # fund_list = Dividend_Yield.objects.raw('select valuation_dividend_yield.id, max(valuation_dividend_yield.period) as period, valuation_dividend_yield.div_yield,\
    #                                             valuation_dividend_yield.short_name_id , valuation_general_information.full_name from valuation_dividend_yield\
    #                                             join valuation_general_information on valuation_dividend_yield.short_name_id = valuation_general_information.short_name\
    #                                             group by short_name_id\
    #                                             order by div_yield DESC, period DESC\
    #                                             limit 5')
    
    best_fund = Dividend_Yield.objects.raw('select valuation_fair_value.id, valuation_fair_value.period_id,\
                                            valuation_fair_value.short_name_id, valuation_fair_value.fair,\
                                            valuation_fair_value.price\
                                            from valuation_fair_value\
                                            inner join (select valuation_dividend_yield.short_name_id\
                                                            from valuation_dividend_yield\
                                                            order by valuation_dividend_yield.period_id desc, valuation_dividend_yield.div_yield desc\
                                                            limit 1) as highest_yield\
                                            on valuation_fair_value.short_name_id = highest_yield.short_name_id')

    # best_fund = Fair_Value.objects.raw('select id, short_name_id, period, price, fair\
    #                                                 from valuation_fair_value\
    #                                                 where short_name_id = (select short_name_id from valuation_dividend_yield\
    #                                                                         order by div_yield DESC limit 1)\
    #                                                 group by short_name_id, period')

    data = \
        DataPool(series=
            [{'options': {
                'source': best_fund},
                'terms': [
                    'period_id','price','fair','short_name_id']}
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
                'period_id':['price'],
                }},
         {'options':{
                'type': 'line',
                'stacking' : False,
                'dashStyle' : 'longdash',
                'color': '#000000'},
            'terms':{
                'period_id':['fair']
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
        fund_list = Dividend_Yield.objects.raw('select valuation_dividend_yield.id, valuation_dividend_yield.period_id, valuation_dividend_yield.div_yield,\
                                                valuation_dividend_yield.short_name_id , valuation_general_information.full_name\
                                                from valuation_dividend_yield\
                                                join valuation_general_information on valuation_dividend_yield.short_name_id = valuation_general_information.short_name\
                                                where valuation_dividend_yield.id in (\
                                                                    select max(valuation_dividend_yield.id)\
                                                                    from valuation_dividend_yield\
                                                                    group by valuation_dividend_yield.short_name_id\
                                                                )\
                                                order by valuation_dividend_yield.div_yield DESC')
        return render(request, 'valuation/ranking.html' , {'fund_list':fund_list, 'rank_type':rank_type})

def test_page(request):
    chart_data = Fair_Value.objects.filter(short_name = 'test').select_related().order_by('-period')
    return render(request, 'valuation/test_page.html' , {'chart_data':chart_data})