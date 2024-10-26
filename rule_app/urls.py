from django.urls import path
from . import views

urlpatterns = [
    path('api/create_rule/', views.create_rule_view, name='create_rule'),
    path('api/combine_rules/', views.combine_rules, name='combine_rules'),
    path('api/evaluate_rule/', views.evaluate_rule, name='evaluate_rule'),
    path('', views.home, name='home'),
    path('display_rule/', views.display_rule, name='display_rule'),
    path('combined_display_rule/', views.combined_display_rule, name='combined_display_rule'),
]
