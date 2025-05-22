from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
# user profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone_number = models.CharField(max_length=20, unique=True)
    county = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    # create a user profile by default when user signs up
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()

# automate profile thingy
post_save.connect(create_user_profile, sender=User)

# Registration of new user
class Register(models.Model):
        username = models.CharField(max_length=50)
        first_name = models.CharField(max_length=50)
        last_name = models.CharField(max_length=50)
        gender = models.CharField(max_length=20, null=True)
        date_of_birth = models.DateField()
        phone_number = models.CharField(max_length=13)
        email = models.EmailField(max_length=100)
        password = models.CharField(max_length=100)
        confirm_password = models.CharField(max_length=100)

        def __str__(self):
            return f'{self.first_name} {self.last_name}'

# Login
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

