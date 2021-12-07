from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


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
    profile_pic = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tool_value = models.DecimalField(max_digits=10, decimal_places=2)
    for_sale = models.BooleanField()
    description = models.CharField(max_length=500)
    tool_pic = models.ImageField(blank=True, null=True, upload_to='tool_pics/')
    name = models.CharField(max_length=255)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'


class Borrow_tx(models.Model):
    # Use "delete" code, logic, or SP to make sure borrower cannot be deleted while borrowing tool,
    # make sure that tool cannot be deleted while borrowed
    borrowed_tool = models.ForeignKey(Tool, on_delete=models.RESTRICT)
    borrower = models.ForeignKey(User, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner_approval = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    # stretch
    rating_from_owner = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    rating_from_borrower = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
