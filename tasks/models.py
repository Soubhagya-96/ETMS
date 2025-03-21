from django.db import models
from users.models import EtmsUser


class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    project_code = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='planned'
    )
    progress = models.PositiveIntegerField(
        default=0, help_text="Completion percentage (0-100%)"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    project_manager = models.ForeignKey(
        EtmsUser, on_delete=models.SET_NULL, null=True, 
        related_name='managed_projects'
    )
    team_members = models.ManyToManyField(
        EtmsUser, blank=True, related_name='assigned_projects'
    )
    budget = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    cost_incurred = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    priority_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo'
    )
    priority = models.CharField(
        max_length=10, choices=priority_choices, default='medium'
    )
    assigned_to = models.ForeignKey(
        EtmsUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.project.project_code})"
    