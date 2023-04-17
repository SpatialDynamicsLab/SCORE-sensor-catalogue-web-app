# Generated by Django 4.1.6 on 2023-04-08 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    # dependencies = [
    #     ('catalogue', '0002_alter_deploymentcost_options_alter_order_options_and_more'),
    # ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=65)),
                ('second_name', models.CharField(max_length=65)),
                ('address', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=110)),
                ('country', models.CharField(max_length=110)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.sensor')),
            ],
            options={
                'verbose_name': 'Order Sensor',
                'verbose_name_plural': 'Order Sensors',
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-start_date'], name='orders_orde_start_d_6ce7d3_idx'),
        ),
    ]
