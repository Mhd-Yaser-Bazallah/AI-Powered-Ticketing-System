                                             

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_alter_ticket_team_assignment_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ticket_team_assignment',
            table='Ticket_Team_Assignment',
        ),
    ]
