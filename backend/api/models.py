from datetime import tzinfo
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bicycle(models.Model):
    """Bicycle for renting object"""
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL')
    type = models.CharField(max_length=20)
    wheel_size = models.IntegerField()
    fork = models.CharField(max_length=40)
    description = models.TextField(blank=False)
    price = models.IntegerField()
    image1 = models.ImageField(upload_to="images/bicycles/")
    image2 = models.ImageField(upload_to="images/bicycles/")
    image3 = models.ImageField(upload_to="images/bicycles/")
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


class RentingInfo(models.Model):
    bicycle = models.ForeignKey('Bicycle', on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)


# class CustomUser(AbstractUser):
#     """User who rents bicycle object"""
#     email = None
#     telephone = models.CharField(max_length=15, unique=True, null=True)
#     bank_card = models.ForeignKey('BankCard', on_delete=models.SET_NULL, null=True, related_name="users", to_field='num')
#     profile_photo = models.ImageField(default='images/bicycles/avatar.jpg', upload_to="images/avatars/")

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['first_name', 'username', 'password1', 'password2', 'telephone', 'bank_card']

#     objects = CustomUserManager()

#     class Meta:
#         verbose_name_plural = 'users'
#         db_table = 'auth_users'
#         ordering = ['first_name', 'last_name']

#     def __str__(self):
#         """Function for output info about the user object."""
#         return self.username

#     def get_absolute_url(self):
#         return reverse('card', kwargs={'card_num':self.num})

# class User(AbstractUser):
#     """User who rents bicycle object"""
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     login = models.CharField(max_length=100, unique=True)
#     telephone = models.CharField(max_length=15, unique=True, null=True)
#     password = models.CharField(max_length=100)
#     bank_card = models.ForeignKey('BankCard', on_delete=models.SET_NULL, null=True, related_name="users", to_field='num')
#     profile_photo = models.ImageField(default='images/bicycles/avatar.jpg', upload_to="images/avatars/")
# 
#     class Meta:
#         verbose_name_plural = 'Users'
#         db_table = 'users'
#         ordering = ['first_name', 'last_name']

#     def __str__(self):
#         """Function for output info about the user object."""
#         return self.login

#     def get_absolute_url(self):
#         return reverse('card', kwargs={'card_num':self.num})


# class User(models.Model):
#     """User who rents bicycle object"""
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     login = models.CharField(max_length=100, unique=True)
#     telephone = models.CharField(max_length=15, unique=True, null=True)
#     password = models.CharField(max_length=100)
#     bank_card = models.ForeignKey('BankCard', on_delete=models.SET_NULL, null=True, related_name="users", to_field='num')
#     profile_photo = models.ImageField(default='images/bicycles/avatar.jpg', upload_to="images/avatars/")

#     class Meta:
#         verbose_name_plural = 'Users'
#         db_table = 'users'
#         ordering = ['first_name', 'last_name']

#     def __str__(self):
#         """Function for output info about the user object."""
#         return self.login

#     def get_absolute_url(self):
#         return reverse('card', kwargs={'card_num':self.num})


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

