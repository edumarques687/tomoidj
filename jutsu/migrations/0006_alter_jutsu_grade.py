# Generated by Django 4.0 on 2022-01-05 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jutsu', '0005_alter_jutsu_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jutsu',
            name='grade',
            field=models.CharField(choices=[('BA', 'Básico'), ('ME', 'Mediano'), ('AV', 'Avançado'), ('SU', 'Sublime'), ('LE', 'Lendário')], default='SU', max_length=2),
        ),
    ]
