from django.db import models
from django.db.models import F
from django.http import Http404
from decimal import Decimal

#fixed dropdown for period input
Period_Choice = (
    ('Jan', 'January'),
    ('Feb', 'February'),
    ('Mar', 'March'),
    ('Apr', 'April'),
    ('May', 'May'),
    ('Jun', 'June'),
    ('Jul', 'July'),
    ('Aug', 'August'),
    ('Sep', 'September'),
    ('Oct', 'October'),
    ('Nov', 'November'),
    ('Dec', 'December')
)

Quarter_Choice = (
    ('Q1','Q1'),
    ('Q2','Q2'),
    ('Q3','Q3'),
    ('Q4','Q4')
)

# Create your models here.
class General_Information(models.Model):
    short_name = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=100)

    #fixed dropdown for fund_type
    LEASE_FREE = 'Leasehold & Freehold'
    LEASE = 'Leasehold'
    FREE = 'Freehold'
    Fund_Type_Choices = (
        (LEASE_FREE, 'Leasehold & Freehold'),
        (LEASE, 'Leasehold'),
        (FREE, 'Freehold'),
    )
    fund_type = models.CharField(max_length=20, choices=Fund_Type_Choices, default=LEASE)

    property_type = models.CharField(max_length=50)
    ipo_date = models.IntegerField()
    dividend_payout_amount_per_year = models.SmallIntegerField()
    listed_share = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    #rename object when call via API
    def __str__(self):
        return self.short_name

#stability calculation api
class YieldManager(models.Manager):
    #stability1
    def get_stability1(self,fund_name):
        try:
            historical_yield = Dividend_Yield.objects.filter(short_name = fund_name)

            #yield avg calculation
            sum_yield = 0
            counter = 0
            for each in historical_yield:
                sum_yield += each.div_yield
                counter += 1
            
            avg = sum_yield/counter

            #get latest yield
            latest_yield = Dividend_Yield.objects.filter(short_name = fund_name).latest('period')
            
            stability1 = '{0:.3g}'.format(latest_yield.div_yield - avg)
            stability1 = Decimal(stability1)

            return stability1
        except:
            return "unavailable"
    
    #stability2
    def get_stability2(self,fund_name):
        try:
            latest_year_yield = Dividend_Yield.objects.filter(short_name = fund_name).order_by('-period')[:4]
            former_year_yield = Dividend_Yield.objects.filter(short_name = fund_name).order_by('-period')[4:][:4]

            #avg latest_year
            counter = 0
            sum_yield = 0
            for each in latest_year_yield:
                sum_yield += each.div_yield
                counter += 1
            
            latest_avg = sum_yield/counter

            #avg former_year
            counter = 0
            sum_yield = 0
            for each in former_year_yield:
                sum_yield += each.div_yield
                counter += 1
            
            former_avg = sum_yield/counter

            stability2 = '{0:.3g}'.format(latest_avg - former_avg)
            stability2 = Decimal(stability2)

            return stability2
        except:
            return "unavailable"

class Dividend_Yield(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False, auto_now_add=False)
    div_yield = models.DecimalField(max_digits=5, decimal_places=2)
    objects = YieldManager()

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Dividend_Payout(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False, auto_now_add=False)
    div_per_share = models.DecimalField(max_digits=8, decimal_places=5)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id
    
class Financial_Statement(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False, auto_now_add=False)
    net_asset = models.DecimalField(max_digits=10, decimal_places=2)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2)
    retained_earning = models.DecimalField(max_digits=10, decimal_places=2)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Financial_Ratio(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False, auto_now_add=False)
    quarter = models.CharField(max_length = 2, choices = Quarter_Choice, null=True)
    eps = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Fair_Value(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.DateField(auto_now=False, auto_now_add=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    fair = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id
