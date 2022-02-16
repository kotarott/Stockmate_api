# Generated by Django 3.2.8 on 2022-02-12 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20220212_0455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keymetric',
            old_name='peRation',
            new_name='peRatio',
        ),
        migrations.AddField(
            model_name='keymetric',
            name='ajustment',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='keymetric',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keymetric',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keymetric',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]