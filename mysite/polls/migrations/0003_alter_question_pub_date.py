# Generated by Django 4.1.7 on 2023-05-13 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_alter_question_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(null=True, verbose_name="date published"),
        ),
    ]
