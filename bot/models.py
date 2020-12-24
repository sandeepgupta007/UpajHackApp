from django.db import models

# Create your models here.

class Farmer(models.Model):
    name = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=14, null=False)
    crop_name = models.CharField(max_length = 30,null = False)
    price = models.IntegerField(null=False)

    def __str__(self):
        return str('{}-{}'.format(self.name, self.crop_name))


class Trader(models.Model):
    name = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=14, null=False)
    crop_name = models.CharField(max_length = 30,null = False)
    price = models.IntegerField(null=False)

    def __str__(self):
        return str('{}-{}'.format(self.name, self.crop_name))