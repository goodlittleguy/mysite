# Generated by Django 2.2 on 2020-08-03 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200804_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readnum',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
        ),
    ]