# Generated by Django 2.1.5 on 2019-02-06 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20190206_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courseenrollments', to='courses.Course', verbose_name='Curso'),
        ),
    ]