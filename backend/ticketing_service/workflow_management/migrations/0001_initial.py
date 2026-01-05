                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('users_management', '0002_customuser_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Workflow', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workflow', to='company.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users_management.customuser')),
            ],
            options={
                'db_table': 'workflow',
            },
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField()),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='workflow_management.workflow')),
            ],
            options={
                'db_table': 'workflow_step',
                'ordering': ['order'],
                'unique_together': {('workflow', 'order')},
            },
        ),
    ]
