# Generated by Django 2.2 on 2019-06-23 03:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('black_list', models.ManyToManyField(blank=True, related_name='rooms_forbidden', to='accounts.UserProfile')),
                ('host', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='accounts.UserProfile')),
                ('members', models.ManyToManyField(blank=True, related_name='room_memberships', to='accounts.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, default=uuid.uuid1, unique=True)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Room')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='accounts.UserProfile')),
            ],
        ),
    ]
