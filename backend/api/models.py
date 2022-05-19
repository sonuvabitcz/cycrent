from django.db import models

class Recipe(models.Model):
    """Recipe object"""
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    ingredients = models.CharField(max_length=255)
   # display an instance of the model when necessary
    def __str__(self):
        return self.title


class User(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)
    address = models.CharField(max_length=250)

    class Meta:
        db_table = "user"
        app_label = ''

    def __str__(self):
        return self