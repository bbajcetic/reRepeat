# Generated by Django 2.1.4 on 2019-01-29 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reRepeat', '0008_auto_20190129_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=1000, verbose_name='Question'),
        ),
    ]
