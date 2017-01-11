from django.db import models

# Create your models here.
class General_Information(models.Model):
    short_name = models.CharField(primary_key=True , max_length = 10)
    full_name = models.CharField(max_length = 100)
    fund_type = models.CharField(max_length = 20)
    property_type = models.CharField(max_length = 50)
    ipo_date = models.IntegerField()
    dividend_payout_per_year = models.SmallIntegerField()

class Dividend_Yield(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    quarter = models.CharField(max_length = 10)
    div_yield = models.DecimalField(max_digits=5 , decimal_places=2)

class Dividend_Payout(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    quarter = models.CharField(max_length = 10)
    div_per_share = models.DecimalField(max_digits=8 , decimal_places=5)

class Financial_Statement(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    quarter = models.CharField(max_length = 10)
    net_asset = models.DecimalField(max_digits=10 , decimal_places=2)
    net_profit = models.DecimalField(max_digits=10 , decimal_places=2)
    rental_income = models.DecimalField(max_digits=10 , decimal_places=2)
    retained_earning = models.DecimalField(max_digits=10 , decimal_places=2)

class Financial_Ratio(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    roe = models.DecimalField(max_digits=5 , decimal_places=2)
    beta = models.DecimalField(max_digits=5 , decimal_places=2)
    stability1 = models.DecimalField(max_digits=5 , decimal_places=2)
    stability2 = models.DecimalField(max_digits=5 , decimal_places=2)