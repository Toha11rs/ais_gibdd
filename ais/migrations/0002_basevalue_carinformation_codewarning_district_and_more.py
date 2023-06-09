# Generated by Django 4.1.7 on 2023-06-09 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BaseValue', models.IntegerField()),
            ],
            options={
                'db_table': 'base_value',
            },
        ),
        migrations.CreateModel(
            name='CarInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=50)),
                ('Brand', models.CharField(max_length=50)),
                ('Model', models.CharField(max_length=50)),
                ('Color', models.CharField(max_length=50)),
                ('Year', models.IntegerField()),
                ('RegistrationDate', models.DateField()),
            ],
            options={
                'db_table': 'carInformation',
            },
        ),
        migrations.CreateModel(
            name='CodeWarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Code', models.IntegerField()),
            ],
            options={
                'db_table': 'code',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('District', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='DriverAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('City', models.CharField(max_length=50)),
                ('Street', models.CharField(max_length=50)),
                ('House', models.IntegerField()),
                ('Flat', models.IntegerField()),
            ],
            options={
                'db_table': 'driver_address',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('patronimyc', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='GetWarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GetWarning', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'warning',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Position', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='StatusPenalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StatusPenalty', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'status_penalty',
            },
        ),
        migrations.CreateModel(
            name='TypeWarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'type',
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='Patronymic',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.codewarning')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.driver')),
                ('typeWarning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.typewarning')),
                ('warning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.getwarning')),
            ],
            options={
                'db_table': 'violation',
            },
        ),
        migrations.CreateModel(
            name='UserTryLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_number', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_try_login',
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PeymantPenalty', models.IntegerField()),
                ('DateTime', models.DateField()),
                ('deprivationDriving', models.IntegerField()),
                ('baseValue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.basevalue')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.codewarning')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.district')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.driver')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.employee')),
                ('statusPenalty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.statuspenalty')),
                ('typeWarning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.typewarning')),
                ('warning', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.getwarning')),
            ],
            options={
                'db_table': 'penalty',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='Position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.position'),
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carinformation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.carinformation')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ais.driver')),
            ],
            options={
                'db_table': 'car',
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='address',
            field=models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, to='ais.driveraddress'),
        ),
    ]
