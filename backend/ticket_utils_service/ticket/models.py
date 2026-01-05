from django.db import models


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auto_prioritize = models.BooleanField(default=True)
    auto_categorize = models.BooleanField(default=True)
    auto_assign = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Company"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.company.name if self.company else 'No Company'} - {self.category}"

    class Meta:
        db_table = "Team"


class Ticket(models.Model):
    document = models.TextField(db_column="Document")
    topic_group = models.CharField(max_length=255, db_column="Topic_group")

    class Meta:
        db_table = "Ticket"
        managed = False


class AnalyzeCounter(models.Model):
    count = models.IntegerField(default=0)
    is_training = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "AnalyzeCounter"
