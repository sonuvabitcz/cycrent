from datetime import tzinfo
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Bicycle(models.Model):
    """Bicycle for renting object"""
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL', blank=True)
    type = models.CharField(max_length=20)
    wheel_size = models.IntegerField()
    fork = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    price = models.IntegerField()
    image1 = models.ImageField(upload_to="images/bicycles/", blank=True)
    image2 = models.ImageField(upload_to="images/bicycles/", blank=True)
    image3 = models.ImageField(upload_to="images/bicycles/", blank=True)
    renting_users = models.ManyToManyField(User, through='RentingInfo', related_name='bicycles')

    class Meta:
        db_table = 'bicycles'
        ordering = ['brand', 'model']

    def __str__(self):
        """Funtion for output info about the bicycle object."""
        return f"{self.brand} {self.model}"
        # return "%s %s" % (self.brand, self.model)

    def get_absolute_url(self):
        return reverse('bicycle', kwargs={'bic_slug':self.slug})

    def save(self, *args, **kwargs):
        slug = self.brand + " " + self.model
        self.slug = slugify(slug)
        super(Bicycle, self).save(*args, **kwargs)


class RentingInfo(models.Model):
    bicycle = models.ForeignKey('Bicycle', on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="rents", blank=True)
    time_get = models.DateTimeField()
    time_return = models.DateTimeField()
    total_price = models.IntegerField()
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('my_one_bicycle', kwargs={'pk':self.pk})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(default=3000)
    date_register = models.DateField(auto_now_add=True)
    # profile_photo = models.ImageField(default='images/bicycles/avatar.jpg', upload_to="images/avatars/")

# users = User.objects.all().select_related('profile') # fast accessing to database https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

# methods call when user is saved or created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class BankCard(models.Model):
#     num = models.CharField(max_length=16, unique=True)
#     ccv = models.IntegerField()
#     money = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'bankcards'
#         ordering = ['num']

#     def __str__(self):
#         """
#         Function for output info about the user object.
#         """
#         return self.num

#     def get_absolute_url(self):
#         return reverse('card', kwargs={'card_num':self.num})

