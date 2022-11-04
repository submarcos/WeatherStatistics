# Generated by Django 4.1.2 on 2022-11-04 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cumulus", "0002_dailydata_alter_data_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="dailydata",
            name="avg_wind_direction",
            field=models.CharField(default="", max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="data",
            name="daily_data",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cumulus.dailydata",
            ),
        ),
    ]
