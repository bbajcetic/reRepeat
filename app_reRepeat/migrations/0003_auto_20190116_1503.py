# Generated by Django 2.1.4 on 2019-01-16 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reRepeat', '0002_auto_20190115_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_text',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=200),
        ),
    ]
