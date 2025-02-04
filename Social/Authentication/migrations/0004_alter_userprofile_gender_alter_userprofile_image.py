# Generated by Django 5.0.2 on 2024-04-27 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_remove_userprofile_p_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
