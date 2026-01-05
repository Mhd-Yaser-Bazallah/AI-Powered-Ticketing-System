                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='embedding',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
