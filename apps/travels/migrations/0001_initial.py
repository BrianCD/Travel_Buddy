# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_remove_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=10000)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('planner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_trips', to='users.User')),
                ('travellers', models.ManyToManyField(blank=True, related_name='joined_trips', to='users.User')),
            ],
        ),
    ]