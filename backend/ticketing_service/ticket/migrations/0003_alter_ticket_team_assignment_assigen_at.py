                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_ticket_priority_alter_ticket_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_team_assignment',
            name='assigen_at',
            field=models.DateField(auto_now=True),
        ),
    ]
