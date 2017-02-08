from django.db import models
from django.db.models import F

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

# Create your models here.
class General_Information(models.Model):
    short_name = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=100)

    #fixed dropdown for fund_type
    LEASE_FREE = 'LF'
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
    latest_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    #rename object when call via API
    def __str__(self):
        return self.short_name

class Dividend_Yield(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period_Choice, default='Jan')
    year = models.IntegerField(null=True)
    div_yield = models.DecimalField(max_digits=5, decimal_places=2)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Dividend_Payout(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period_Choice, default='Jan')
    year = models.IntegerField(null=True)
    div_per_share = models.DecimalField(max_digits=8, decimal_places=5)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id
    
class Financial_Statement(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period_Choice, default='Jan')
    year = models.IntegerField(null=True)
    net_asset = models.DecimalField(max_digits=10, decimal_places=2)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2)
    retained_earning = models.DecimalField(max_digits=10, decimal_places=2)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Financial_Ratio(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period_Choice, default='Jan')
    year = models.IntegerField(null=True)
    eps = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    beta = models.DecimalField(max_digits=5, decimal_places=2)
    stability1 = models.DecimalField(max_digits=5, decimal_places=2)
    stability2 = models.DecimalField(max_digits=5, decimal_places=2)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id

class Fair_Value(models.Model):
    short_name = models.ForeignKey(General_Information, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=Period_Choice, default='Jan')
    year = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    fair = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    #rename object when call via API
    def __str__(self):
        return self.short_name_id
