# Generated by Django 4.1.5 on 2023-03-22 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_first_name_alter_customuser_id'),
        ('mainlobby', '0005_product_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('stripe_customer_id', models.CharField(max_length=120)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
