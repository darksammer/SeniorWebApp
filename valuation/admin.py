from django.contrib import admin
from .models import *

#Admin class for General_Information
class GeneralAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'full_name', 'fund_type')

#Admin class for Dividend_Yield
class YieldAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'quarter', 'div_yield')

#Admin class for Dividend_Payout
class PayoutAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'quarter', 'div_per_share')

#Admin class for Financial_Statement
class StatementAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'quarter', 'net_asset', 'net_profit', 'rental_income', 'retained_earning')

#Admin class for Financial_Ratio
class RatioAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'quarter', 'roe', 'beta', 'stability1', 'stability2')

# Register your models here.
admin.site.register(General_Information, GeneralAdmin)
admin.site.register(Dividend_Yield, YieldAdmin)
admin.site.register(Dividend_Payout, PayoutAdmin)
admin.site.register(Financial_Statement, StatementAdmin)
admin.site.register(Financial_Ratio, RatioAdmin)