from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    cc_fullname = models.CharField(max_length=255, null=True)
    cc_number = models.CharField(max_length=22, null=True)
    cc_exp = models.CharField(max_length=5, null=True)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    img_url = models.CharField(max_length=255, null=True)
    tac_agree = models.BooleanField(blank=False)


class Tool(models.Model):
    ownerID = models.ForeignKey(User, on_delete=models.CASCADE)
    tool_value = models.DecimalField(max_digits=10, decimal_places=2)
    for_sale = models.BooleanField()
    description = models.CharField(max_length=500)
    img_url = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    visible = models.BooleanField(default=True)


class Borrow_tx(models.Model):
    # Use "delete" code, logic, or SP to make sure borrower cannot be deleted while borrowing tool,
    # make sure that tool cannot be deleted while borrowed
    toolID = models.ForeignKey(Tool, on_delete=models.RESTRICT)
    borrowerID = models.IntegerField() 
    timestamp = models.DateTimeField()
    returned = models.BooleanField(default=False)
    # stretch
    rating_from_owner = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    rating_from_borrower = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
