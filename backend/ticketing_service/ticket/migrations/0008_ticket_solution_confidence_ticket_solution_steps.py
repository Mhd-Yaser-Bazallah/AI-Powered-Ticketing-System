                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_ticket_bert_category_ticket_bert_confidence_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='solution_confidence',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='solution_steps',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
