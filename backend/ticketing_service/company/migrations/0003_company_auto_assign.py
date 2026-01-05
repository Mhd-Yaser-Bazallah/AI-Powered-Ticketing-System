                                               

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_company_auto_categorize_company_auto_prioritize'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='auto_assign',
            field=models.BooleanField(default=True),
        ),
    ]
