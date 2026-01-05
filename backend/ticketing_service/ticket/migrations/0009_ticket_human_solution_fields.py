from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users_management", "0001_initial"),
        ("ticket", "0008_ticket_solution_confidence_ticket_solution_steps"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="human_solution_steps",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ticket",
            name="human_solved_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ticket",
            name="human_solved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="human_solved_tickets",
                to="users_management.customuser",
            ),
        ),
    ]
