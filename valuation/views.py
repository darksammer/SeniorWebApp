from django.shortcuts import render,render_to_response, redirect
from django.http import Http404
from django.db.models import F
from django.utils import timezone
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
    
    current_year = timezone.now().year-6

    #fund age
    age = current_year - fund_data.ipo_date

    #get dividend stability
    stability1 = Dividend_Yield.objects.get_stability1(fund_name = name)
    stability2 = Dividend_Yield.objects.get_stability2(fund_name = name)

    if (stability1 >= -1 and stability1 <= 2) and (stability2 >= -1 and stability2 <= 2):
        stability_status = "Consistent"
    elif stability1 < -1 or stability2 < -1:
        stability_status = "Declined"
    else:
        stability_status = "Growth"

    #detect payout consistent
    historical_yield = Dividend_Yield.objects.filter(short_name = name).filter(period__year = current_year-1)
    dividend_status =  len(historical_yield) / fund_data.dividend_payout_amount_per_year

    if dividend_status == 1:
        payout_consistent = 'Consistent'
    elif dividend_status > 1:
        payout_consistent = 'More than usual'
    else:
        payout_consistent = 'Zero payout detected in last year'

    #Retained Earning
    retained = Financial_Statement.objects.filter(short_name = name).filter(period__year = current_year-1).filter(quarter = 'Q4')

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

    
    return render(request,'valuation/fund.html',{'name': name, 'age':age, 'fund_data':fund_data,
                                                    'chart':value_chart, 
                                                    'payout_consistent':payout_consistent, 'retained':retained,
                                                    'stability_status':stability_status,
                                                    'stability1':stability1, 'stability2':stability2})

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