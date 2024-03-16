from django.db import models
# Create your models here.


class Drinks(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    type_is_hot = models.BooleanField(default=True)


class Desserts(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField(default=0)
    composition = models.CharField()


class WorkingHours(models.Model):
    day_name = models.CharField(max_length=64)
    start_of_work = models.TimeField()
    end_of_work = models.TimeField()


class InformationAboutCoffeeShop(models.Model):
    adres = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    work_schedule = models.OneToOneField(WorkingHours, on_delete=models.CASCADE)
    district = models.CharField(max_length=128)
    ranking = models.FloatField(default=0)


class CoffeeShop(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    drinks = models.ForeignKey(Drinks, on_delete=models.CASCADE)
    desserts = models.ForeignKey(Desserts, on_delete=models.CASCADE)
    info = models.OneToOneField(InformationAboutCoffeeShop, on_delete=models.CASCADE)


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True)
    favourite_cafes = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    favourite_desserts = models.ForeignKey(Desserts, on_delete=models.CASCADE)
    favourite_drinks = models.ForeignKey(Drinks, on_delete=models.CASCADE)


class Feedback(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    coffees = models.ManyToManyField(CoffeeShop, null=True)
    rating = models.OneToOneField(User, on_delete=models.CASCADE)

