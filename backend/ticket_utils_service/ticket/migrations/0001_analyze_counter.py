from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnalyzeCounter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("count", models.IntegerField(default=0)),
                ("is_training", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_triggered_at", models.DateTimeField(blank=True, null=True)),
                ("last_error", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "AnalyzeCounter",
            },
        ),
    ]
