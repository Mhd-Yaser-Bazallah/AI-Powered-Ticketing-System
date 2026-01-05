                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ticket', '0001_initial'),
        ('users_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.customuser')),
            ],
            options={
                'db_table': 'Comments',
                'ordering': ['created_at'],
            },
        ),
    ]
