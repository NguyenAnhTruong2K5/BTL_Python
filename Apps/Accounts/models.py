from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone
class Customer(models.Model):
    cccd = models.CharField(max_length=20, primary_key= True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length= 100, null= True,)
    phone_number = models.CharField(max_length=20, unique=True, null= False)


class Contract(models.Model):
    plate_number = models.CharField(max_length=20, primary_key= True)
    vehicle_type = models.CharField(max_length=100, null= False, blank= False)
    cccd = models.OneToOneField('Customer', on_delete=models.CASCADE, to_field= 'cccd', db_column= 'cccd')
    term = models.CharField(max_length=10, choices= [('monthly', 'Monthly'), ('yearly', 'Yearly')])
    duration = models.IntegerField()
    start_date = models.DateField(default= timezone.now)
    end_date = models.DateField(blank= True, editable= False, null= True)

    def save(self, *args, **kwargs):
        print("Calculating end_date based on term and duration...")
        if self.term == 'monthly':
            self.end_date = self.start_date + relativedelta(months= self.duration)
        elif self.term == 'yearly':
            self.end_date = self.start_date + relativedelta(years= self.duration)
        super().save(*args, **kwargs)

