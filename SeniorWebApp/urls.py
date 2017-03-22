"""SeniorWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from SeniorWebApp import settings

from valuation import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index_view, name='index'),
    url(r'^search/',views.search_view, name='search'),
    url(r'^ranking/(?P<rank_type>\w+)/',views.ranking_view, name='ranking'),
    url(r'^fund/(?P<name>\w+)/$',views.fund_view, name='fund'),
    url(r'^test_page/',views.test_page, name='test'),
]
