                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_log', '0002_ticketlog_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketlog',
            name='comments',
            field=models.CharField(max_length=50),
        ),
    ]
