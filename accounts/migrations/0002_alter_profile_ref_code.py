# Generated by Django 4.0.4 on 2022-05-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ref_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]