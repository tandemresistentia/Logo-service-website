from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
def contact_default():
    return 'In Progress'
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null = True, blank = True)
    completed = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Delivered', 'Delivered'),
    ('Completed', 'Completed'),
    ]
    complete = models.CharField(max_length=20,
        choices=completed,
        default=contact_default(),
    )
    transaction_id = models.CharField(max_length=100)
    url = models.CharField(max_length=600)
    item_description = models.CharField(max_length=1000)
    license_file = models.FileField(upload_to='myfiles/',blank=True,null = True)
    revisions_data = models.IntegerField(null = True)
    def __str__(self):
        return f'{self.user.username} {self.date_created}'
