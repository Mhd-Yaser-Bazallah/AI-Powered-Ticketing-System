                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='auto_categorize',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='company',
            name='auto_prioritize',
            field=models.BooleanField(default=True),
        ),
    ]
