# Generated by Django 5.0.6 on 2024-06-18 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel", "0019_alter_post_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=30, unique=True, verbose_name="標籤名稱"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                related_name="posts", to="travel.tag", verbose_name="標籤"
            ),
        ),
    ]
