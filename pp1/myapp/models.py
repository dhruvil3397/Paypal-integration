from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    paypal_email = models.CharField(max_length=40,blank=True,null=True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)