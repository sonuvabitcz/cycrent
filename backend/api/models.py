from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Bicycle(models.Model):
    """Bicycle for renting object"""
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20)
    wheel_size = models.IntegerField()
    fork = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    price = models.IntegerField()
    image1 = models.ImageField(upload_to="images/bicycles/%Y/%m/%d/")
    image2 = models.ImageField(upload_to="images/bicycles/%Y/%m/%d/")
    image3 = models.ImageField(upload_to="images/bicycles/%Y/%m/%d/")
    renting_users = models.ManyToManyField('User', through='RentingInfo', related_name='bicycles')

    class Meta:
        db_table = 'bicycles'
        ordering = ['brand', 'model']

    def __str__(self):
        """Funtion for output info about the bicycle object."""
        return f"{self.brand} {self.model}"
        # return "%s %s" % (self.brand, self.model)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id':self.pk})


class User(models.Model):
    """User who rents bicycle object"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login = models.CharField(max_length=100, unique=True)
    telephone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    bank_card = models.ForeignKey('BankCard', on_delete=models.SET_NULL, null=True, related_name='+', to_field='num')
    profile_photo = models.ImageField(default='images/profiles/avatar.png', upload_to="images/%Y/%m/%d/")

    class Meta:
        db_table = 'users'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        """Function for output info about the user object."""
        return self.login


class BankCard(models.Model):
    num = models.CharField(max_length=16, unique=True)
    ccv = models.IntegerField()
    money = models.IntegerField(default=0)

    class Meta:
        db_table = 'bankcards'
        ordering = ['num']

    def __str__(self):
        """Function for output info about the user object."""
        return self.num


class RentingInfo(models.Model):
    bicycle = models.ForeignKey('Bicycle', on_delete=models.CASCADE, default=None)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    time_get = models.DateTimeField()
    time_return = models.DateTimeField()
    status = models.BooleanField(default=False)