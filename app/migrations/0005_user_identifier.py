# Generated by Django 4.2 on 2023-04-16 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identifier',
            field=models.CharField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
