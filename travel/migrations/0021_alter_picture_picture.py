# Generated by Django 5.0.6 on 2024-06-18 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel", "0020_tag_post_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="picture",
            name="picture",
            field=models.ImageField(upload_to="pictures/"),
        ),
    ]