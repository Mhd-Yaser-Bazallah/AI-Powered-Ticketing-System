                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('ticket', '0001_initial'),
        ('users_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=255)),
                ('previous_status', models.CharField(max_length=50)),
                ('new_status', models.CharField(max_length=50)),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.comments')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.customuser')),
            ],
            options={
                'db_table': 'TicketLog',
            },
        ),
    ]
