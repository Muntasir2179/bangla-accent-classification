# Generated by Django 4.1.5 on 2023-11-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predicted_accent', models.TextField(max_length=50)),
                ('file_name', models.TextField(max_length=200)),
                ('predicted_accent_confidence', models.FloatField(default=0.0)),
                ('barishal_conf', models.FloatField(default=0.0)),
                ('bogura_conf', models.FloatField(default=0.0)),
                ('chottogram_conf', models.FloatField(default=0.0)),
                ('kurigram_conf', models.FloatField(default=0.0)),
                ('madaripur_conf', models.FloatField(default=0.0)),
                ('mymenshing_conf', models.FloatField(default=0.0)),
                ('noakhali_conf', models.FloatField(default=0.0)),
                ('pabna_conf', models.FloatField(default=0.0)),
                ('puran_dhaka_conf', models.FloatField(default=0.0)),
                ('rajshahi_conf', models.FloatField(default=0.0)),
                ('shatkhira_conf', models.FloatField(default=0.0)),
                ('sylhet_conf', models.FloatField(default=0.0)),
                ('tahurgaon_conf', models.FloatField(default=0.0)),
                ('user_prediction', models.TextField(max_length=50)),
                ('is_correct_prediction', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Accent Data',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
