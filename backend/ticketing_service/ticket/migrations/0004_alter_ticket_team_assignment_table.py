                                             

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_alter_ticket_team_assignment_assigen_at'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ticket_team_assignment',
            table='ticket_team_assignment',
        ),
    ]
