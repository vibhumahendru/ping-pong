# Generated by Django 3.1 on 2020-08-31 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pp_score', '0003_session_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='pp_score.session'),
        ),
    ]