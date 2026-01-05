                                             

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('client', 'Client'), ('support_team_member', 'Support Team Member'), ('support_team_manager', 'Support Team Manager')], default='client', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('password', models.CharField(max_length=128)),
                ('company_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
            options={
                'db_table': 'customuser',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.customuser')),
            ],
            options={
                'db_table': 'Membership',
            },
        ),
    ]
