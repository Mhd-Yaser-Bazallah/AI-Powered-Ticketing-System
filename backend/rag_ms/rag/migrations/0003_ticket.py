                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rag', '0002_processed_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('solution_steps', models.JSONField(blank=True, null=True)),
                ('solution_confidence', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Ticket',
                'managed': False,
            },
        ),
    ]
