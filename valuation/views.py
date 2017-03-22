from django.shortcuts import render,render_to_response, redirect
from django.http import Http404
from django.db.models import F, Prefetch, Max
from django.utils import timezone
from chartit import DataPool, Chart
from .models import *

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
    except:
        raise Http404('Fund not found')
    
    current_year = timezone.now().year

    #fund age
    age = current_year - fund_data.ipo_date

    #get dividend stability
    stability1 = Dividend_Yield.objects.get_stability1(fund_name = name)
    stability2 = Dividend_Yield.objects.get_stability2(fund_name = name)

    try:
        if (stability1 >= -1 and stability1 <= 2) and (stability2 >= -1 and stability2 <= 2):
            stability_status = "Consistent"
        elif stability1 < -1 or stability2 < -1:
            stability_status = "Declined"
        else:
            stability_status = "Growth"
    except:
        stability_status = "Unavailable"

    #detect payout consistent
    historical_yield = Dividend_Yield.objects.prefetch_related(
                                Prefetch(
                                    "period",
                                    queryset = Period_Table.objects.filter(period__year = current_year-1)
                                )
                            ).filter(short_name = name)
    dividend_status =  len(historical_yield) / fund_data.dividend_payout_amount_per_year

    if dividend_status == 1:
        payout_consistent = 'Consistent'
    elif dividend_status > 1:
        payout_consistent = 'More than usual'
    else:
        payout_consistent = 'Zero payout detected in last year'

    #Retained Earning
    statement_data = Financial_Statement.objects.filter(short_name = name).order_by('-period')
    if age < 3:
        retained_status = "No data to compare"
    else:
        first_year_compare = statement_data[0].retained_earning - statement_data[1].retained_earning
        second_year_compare = statement_data[0].retained_earning - statement_data[2].retained_earning

        #first year status
        if abs(first_year_compare) > statement_data[1].retained_earning*10/100:
            if first_year_compare > 0:
                first_year_status = "Growth"
            else:
                first_year_status = "Declined"
        elif abs(first_year_compare) < statement_data[1].retained_earning*10/100 or first_year_compare == 0:
            first_year_status = "Consistent"

        #second year status
        if abs(second_year_compare) > statement_data[2].retained_earning*10/100:
            if second_year_compare > 0:
                second_year_status = "Growth"
            else:
                second_year_status = "Declined"
        elif abs(second_year_compare) < statement_data[2].retained_earning*10/100 or second_year_compare == 0:
            second_year_status = "Consistent"

        #retained result
        if first_year_status == "Growth" and second_year_status == "Growth":
            retained_status = "Growth"
        elif (first_year_status == "Growth" and second_year_status == "Declined") or (second_year_status == "Growth" and first_year_status == "Declined"):
            retained_status = "Fluctuation"
        elif first_year_status == "Declined" and second_year_status == "Declined":
            retained_status = "Declined"
        else:
            retained_status = "Consistent"

    #Rental Income
    if age < 3:
        rental_status = "No data to compare"
    else:
        first_year_compare = statement_data[0].rental_income - statement_data[1].rental_income
        second_year_compare = statement_data[0].rental_income - statement_data[2].rental_income

        #first year status
        if abs(first_year_compare) > statement_data[1].rental_income*5/100:
            if first_year_compare > 0:
                first_year_status = "Growth"
            else:
                first_year_status = "Declined"
        elif abs(first_year_compare) < statement_data[1].rental_income*5/100 or first_year_compare == 0:
            first_year_status = "Consistent"

        #second year status
        if abs(second_year_compare) > statement_data[2].rental_income*5/100:
            if second_year_compare > 0:
                second_year_status = "Growth"
            else:
                second_year_status = "Declined"
        elif abs(second_year_compare) < statement_data[2].rental_income*5/100 or second_year_compare == 0:
            second_year_status = "Consistent"

        #rental result
        if first_year_status == "Growth" and second_year_status == "Growth":
            rental_status = "Growth"
        elif (first_year_status == "Growth" and second_year_status == "Declined") or (second_year_status == "Growth" and first_year_status == "Declined"):
            rental_status = "Fluctuation"
        elif (first_year_status == "Declined" and second_year_status == "Declined") or\
            (first_year_status == "Declined" and second_year_status == "Consistent") or\
            (first_year_status == "Consistent" and second_year_status == "Declined"):
            rental_status = "Declined"
        else:
            rental_status = "Consistent"


    data = \
        DataPool(series=
            [{'options': {
                'source': Fair_Value.objects.filter(short_name = name).select_related()},
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
                                                    'payout_consistent':payout_consistent, 'statement':statement_data,
                                                    'stability_status':stability_status, 'retained_status':retained_status,
                                                    'rental_status':rental_status})

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
    current_payout = Dividend_Payout.objects.filter(short_name='test', period='2017-03-01')
    payout_amount = General_Information.objects.filter(short_name='test')

    return render(request, 'valuation/test_page.html' , {'current_payout':current_payout, 'payout_amount':payout_amount})