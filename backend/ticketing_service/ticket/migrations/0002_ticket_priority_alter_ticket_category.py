                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.CharField(default='low', max_length=50),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='category',
            field=models.CharField(default='back', max_length=50),
        ),
    ]
