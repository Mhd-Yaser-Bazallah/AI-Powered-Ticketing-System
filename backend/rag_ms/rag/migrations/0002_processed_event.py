from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rag", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcessedEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_id", models.CharField(max_length=64, unique=True)),
                ("event_type", models.CharField(max_length=100)),
                ("status", models.CharField(choices=[("processing", "processing"), ("completed", "completed"), ("failed", "failed")], default="processing", max_length=20)),
                ("error_message", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
