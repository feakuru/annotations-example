# Generated by Django 3.1 on 2020-08-28 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_labelmeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelmeta',
            name='label',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meta', to='images.label'),
        ),
    ]
