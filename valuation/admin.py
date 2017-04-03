from django.contrib import admin
from .models import *

#Admin class for General_Information
class GeneralAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'full_name', 'fund_type', 'listed_share')

#Admin class for Dividend_Yield
class YieldAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'div_yield')

class FairInLine(admin.TabularInline):
    model = Fair_Value

#Admin class for Dividend_Payout
class PayoutAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'div_per_share')
    #inlines = [FairInLine]

#Admin class for Financial_Statement
class StatementAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'net_asset', 'net_profit', 'rental_income', 'retained_earning')

#Admin class for Financial_Ratio
class RatioAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'eps')

#Admin class for Fair_Value
class FairAdmin(admin.ModelAdmin):
    search_fields = ['short_name']
    list_display = ('short_name', 'period', 'price', 'ddm_fair', 'fair', 'yield_status', 'payout_status', 'rental_status', 'retained_status')
    #readonly_fields = ('fair',)

# Register your models here.
admin.site.register(General_Information, GeneralAdmin)
admin.site.register(Dividend_Yield, YieldAdmin)
admin.site.register(Dividend_Payout, PayoutAdmin)
admin.site.register(Financial_Statement, StatementAdmin)
admin.site.register(Financial_Ratio, RatioAdmin)
admin.site.register(Fair_Value, FairAdmin)
admin.site.register(Period_Table)