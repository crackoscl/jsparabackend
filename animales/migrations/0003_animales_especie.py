# Generated by Django 3.1.3 on 2020-11-23 14:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('animales', '0002_auto_20201123_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='animales',
            name='especie',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]