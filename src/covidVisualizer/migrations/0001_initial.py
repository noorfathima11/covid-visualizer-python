# Generated by Django 3.0.3 on 2020-07-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataFrame',
            fields=[
                ('id', models.IntegerField()),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('population', models.IntegerField(default=0)),
                ('namecode', models.CharField(max_length=10)),
                ('confirmed', models.IntegerField(default=0)),
                ('deceased', models.IntegerField(default=0)),
                ('recovered', models.IntegerField(default=0)),
                ('tested', models.IntegerField(default=0)),
            ],
        ),
    ]
