# Generated by Django 5.1.3 on 2024-11-27 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('column', models.IntegerField()),
                ('value', models.IntegerField(default=0)),
                ('solution', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('sudoku_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='sudoku_app.sudokugames')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_value', models.IntegerField()),
                ('new_value', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='sudoku_app.cell')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='sudoku_app.sessions')),
            ],
        ),
        migrations.AddField(
            model_name='cell',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='sudoku_app.sessions'),
        ),
    ]
