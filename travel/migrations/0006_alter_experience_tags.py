# Generated by Django 5.0.6 on 2024-05-28 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_photo_image_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='experiences', to='travel.tag', verbose_name='標籤'),
        ),
    ]