                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_alter_ticket_team_assignment_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_user_assignment',
            name='assigen_at',
            field=models.DateField(auto_now=True),
        ),
    ]
