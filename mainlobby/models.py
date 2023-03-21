from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    #description
    price = models.FloatField(null=True)
    active = models.BooleanField(null=True)
    image = models.ImageField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)