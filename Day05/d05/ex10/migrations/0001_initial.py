# Generated by Django 5.0.6 on 2024-06-11 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('birth_year', models.CharField(blank=True, max_length=32, null=True)),
                ('gender', models.CharField(blank=True, max_length=32, null=True)),
                ('eye_color', models.CharField(blank=True, max_length=32, null=True)),
                ('hair_color', models.CharField(blank=True, max_length=32, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('mass', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ex10_People',
            },
        ),
        migrations.CreateModel(
            name='Planets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('climate', models.CharField(blank=True, max_length=255, null=True)),
                ('diameter', models.IntegerField(blank=True, null=True)),
                ('orbital_period', models.IntegerField(blank=True, null=True)),
                ('population', models.BigIntegerField(blank=True, null=True)),
                ('rotation_period', models.IntegerField(blank=True, null=True)),
                ('surface_water', models.FloatField(blank=True, null=True)),
                ('terrain', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ex10_Planets',
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('title', models.CharField(max_length=64, unique=True)),
                ('episode_nb', models.IntegerField(primary_key=True, serialize=False)),
                ('opening_crawl', models.TextField(null=True)),
                ('director', models.CharField(max_length=32)),
                ('producer', models.CharField(max_length=128)),
                ('release_date', models.DateField()),
                ('characters', models.ManyToManyField(related_name='movies', to='ex10.people')),
            ],
            options={
                'db_table': 'ex10_Movies',
            },
        ),
        migrations.AddField(
            model_name='people',
            name='homeworld',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ex10.planets'),
        ),
    ]
