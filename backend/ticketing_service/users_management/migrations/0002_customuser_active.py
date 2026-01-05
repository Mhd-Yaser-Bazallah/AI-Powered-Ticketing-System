                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
