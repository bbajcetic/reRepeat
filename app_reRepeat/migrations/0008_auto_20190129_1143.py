# Generated by Django 2.1.4 on 2019-01-29 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reRepeat', '0007_auto_20190127_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=500, verbose_name='Question'),
        ),
    ]