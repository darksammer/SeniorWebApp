from django.contrib import admin
from .models import *

# Register your models here.
admin.register(General_Information , Dividend_Yield , Dividend_Payout , Financial_Statement , Financial_Ratio)(admin.ModelAdmin)