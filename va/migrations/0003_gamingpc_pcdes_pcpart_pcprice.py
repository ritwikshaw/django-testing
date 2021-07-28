# Generated by Django 3.1.1 on 2021-07-28 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('va', '0002_auto_20210718_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pcdes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des1', models.CharField(blank=True, max_length=200, null=True)),
                ('des2', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pcpart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wifi', models.BooleanField(default=True)),
                ('blutooth', models.BooleanField(default=True)),
                ('vr', models.BooleanField(default=True)),
                ('stream', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pcprice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('qua', models.IntegerField()),
                ('ava', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gamingpc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cpu', models.CharField(blank=True, max_length=100, null=True)),
                ('gpu', models.CharField(blank=True, max_length=100, null=True)),
                ('ram', models.CharField(blank=True, max_length=100, null=True)),
                ('des', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='va.pcdes')),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='va.pcpart')),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='va.pcprice')),
            ],
        ),
    ]