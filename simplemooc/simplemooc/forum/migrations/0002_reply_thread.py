# Generated by Django 2.1.5 on 2019-02-24 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='thread',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.Thread', verbose_name='Tópico'),
            preserve_default=False,
        ),
    ]
