# Generated by Django 3.2.8 on 2022-01-30 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_auto_20220130_0149'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]