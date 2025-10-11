from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contracts")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")  # active, expired, cancelled

    def __str__(self):
        return f"Contract {self.contract_id} - {self.customer.full_name}"