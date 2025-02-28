# Generated by Django 3.0.1 on 2020-01-23 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_group_locked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('create_time', models.DateField(auto_now=True)),
                ('check_string', models.CharField(max_length=250)),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Class')),
            ],
        ),
    ]
