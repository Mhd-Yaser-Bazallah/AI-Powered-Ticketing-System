from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        ("files", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="uploadedfile",
            name="company",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="company.company"),
        ),
    ]
