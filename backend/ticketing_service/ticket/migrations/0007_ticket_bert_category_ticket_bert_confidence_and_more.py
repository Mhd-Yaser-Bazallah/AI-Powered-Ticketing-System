                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_alter_ticket_user_assignment_assigen_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='bert_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='bert_confidence',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='need_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='similarity_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
