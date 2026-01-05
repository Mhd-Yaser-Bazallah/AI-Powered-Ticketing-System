                                             

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("file", models.FileField(upload_to="files/")),
                ("original_name", models.CharField(max_length=255)),
                ("kind", models.CharField(choices=[("pdf", "PDF"), ("word", "Word"), ("excel", "Excel")], max_length=10)),
                ("size_bytes", models.BigIntegerField()),
                ("content_type", models.CharField(max_length=100)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "UploadedFile",
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
