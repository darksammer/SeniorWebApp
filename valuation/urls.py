from django.conf.urls import url
from . import views

app_name = 'valuation'
urlpattern = [
    url(r'^$',views.chart_view,name='index'),
]