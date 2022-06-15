# Generated by Django 3.2.13 on 2022-06-15 15:30

import authext.models
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
            ],
            options={
                'verbose_name': '组',
                'verbose_name_plural': '组',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneLogin',
            fields=[
                ('id', models.AutoField(help_text='ID', primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='手机号', max_length=15, unique=True, validators=[authext.models.is_phone_number], verbose_name='手机号')),
                ('user', models.OneToOneField(help_text='用户', on_delete=django.db.models.deletion.CASCADE, to='authext.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '手机登录',
                'verbose_name_plural': '手机登录',
            },
        ),
    ]
