                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('team', '0001_initial'),
        ('users_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField(default='ticket')),
                ('status', models.CharField(default='open', max_length=50)),
                ('category', models.CharField(default='low', max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_ticket', to='users_management.customuser')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
            options={
                'db_table': 'Ticket',
            },
        ),
        migrations.CreateModel(
            name='Ticket_Team_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigen_at', models.DateField()),
                ('Team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('Ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket_User_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigen_at', models.DateField()),
                ('Ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.customuser')),
            ],
            options={
                'db_table': 'Ticket_User_Assignment',
            },
        ),
    ]
