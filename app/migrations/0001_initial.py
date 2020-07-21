# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-30 11:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('label', models.ManyToManyField(blank=True, related_name='note_labels', to='app.Label')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='note',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='app.Notes'),
        ),
    ]
