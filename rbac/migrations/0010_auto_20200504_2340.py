# Generated by Django 2.0 on 2020-05-04 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0009_auto_20200504_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='alias',
            field=models.CharField(max_length=32, unique=True, verbose_name='url别名'),
        ),
    ]