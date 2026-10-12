"""Shared choices and the single definition of an active ticket."""

from django.db import models


class Role(models.TextChoices):
    EMPLOYEE = "Employee", "Employee"
    TECHNICIAN = "Technician", "Technician"
    IT_ADMIN = "IT Admin", "IT Admin"


class Status(models.TextChoices):
    NEW = "new", "New"
    ASSIGNED = "assigned", "Assigned"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"
    CANCELLED = "cancelled", "Cancelled"


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


ACTIVE_STATUSES = (Status.NEW, Status.ASSIGNED, Status.IN_PROGRESS)
TERMINAL_STATUSES = (Status.RESOLVED, Status.CANCELLED)
