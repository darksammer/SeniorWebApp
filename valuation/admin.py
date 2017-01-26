from django.contrib import admin
from .models import *

#Admin class for General_Information
class GeneralAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'full_name', 'fund_type', 'listed_share')

#Admin class for Dividend_Yield
class YieldAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'year', 'div_yield')

#Admin class for Dividend_Payout
class PayoutAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'year', 'div_per_share')

#Admin class for Financial_Statement
class StatementAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'year', 'net_asset', 'net_profit', 'rental_income', 'retained_earning')

#Admin class for Financial_Ratio
class RatioAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'year', 'eps', 'beta', 'stability1', 'stability2')

#Admin class for Fair_Value
class FairAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'year', 'period', 'price', 'fair')

# Register your models here.
admin.site.register(General_Information, GeneralAdmin)
admin.site.register(Dividend_Yield, YieldAdmin)
admin.site.register(Dividend_Payout, PayoutAdmin)
admin.site.register(Financial_Statement, StatementAdmin)
admin.site.register(Financial_Ratio, RatioAdmin)
admin.site.register(Fair_Value, FairAdmin)