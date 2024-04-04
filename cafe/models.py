from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Drinks(models.Model):
    name = models.CharField('Napój', max_length=64)
    price = models.FloatField(default=0)
    type_is_hot = models.BooleanField('Hot drink', default=True)

    def __str__(self):
        return self.name


class Desserts(models.Model):
    name = models.CharField('Deser', max_length=64)
    description = models.TextField()
    price = models.FloatField(default=0)
    composition = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class CoffeeShop(models.Model):
    name = models.CharField('Kawiarnia', max_length=128)
    description = models.TextField()
    drinks = models.ManyToManyField(Drinks)
    desserts = models.ManyToManyField(Desserts)
    adres = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    district = models.CharField(max_length=128)
    ranking = models.FloatField(default=0)
    start_of_work = models.TimeField()
    end_of_work = models.TimeField()

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_cafes = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE, null=True)
    favourite_desserts = models.ForeignKey(Desserts, on_delete=models.CASCADE, null=True)
    favourite_drinks = models.ForeignKey(Drinks, on_delete=models.CASCADE, null=True)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    coffees = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'coffees'], name='feedback_constraints')
        ]

