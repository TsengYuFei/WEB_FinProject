# Generated by Django 5.0.6 on 2024-05-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_alter_experience_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(related_name='experiences', to='travel.tag', verbose_name='標籤'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='會員編號'),
        ),
    ]
