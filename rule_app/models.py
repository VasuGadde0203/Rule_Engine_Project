# rule_app/models.py
from django.db import models

class Rule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rule_string = models.TextField()
    rule = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
