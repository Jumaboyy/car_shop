# Generated by Django 5.0.3 on 2024-05-16 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('image', models.ImageField(upload_to='products', verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product_cart',
                'verbose_name_plural': 'Product_carts',
            },
        ),
    ]