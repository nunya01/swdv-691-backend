from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    # Profile class builds on the included User class without modifying the
    # built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cc_fullname = models.CharField(max_length=255, blank=True, null=True)
    cc_number = models.CharField(max_length=22, blank=True, null=True)
    cc_exp = models.CharField(max_length=5, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    img_url = models.CharField(max_length=255, null=True)
    terms_and_cond = models.BooleanField(default=False)


# These functions update the Profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    rating_from_owner = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    rating_from_borrower = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
