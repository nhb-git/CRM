# Generated by Django 2.0 on 2020-04-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_permission_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='parent_url',
            field=models.ManyToManyField(related_name='_permission_parent_url_+', to='rbac.Permission', verbose_name='父导航标志'),
        ),
    ]