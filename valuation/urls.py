from django.conf.urls import url
from . import views

app_name = 'valuation'
urlpattern = [
    url(r'^$',views.chart_view,name='chart'),
    url(r'^$',views.fund_view,name='fund'),
    url(r'^$',views.index_view,name='index'),
    url(r'^$',views.search_view,name='search')
]