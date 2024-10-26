# rule_app/admin.py
from django.contrib import admin
from .models import Rule

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rule_string', 'rule')
    search_fields = ('name',)