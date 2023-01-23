from django.urls import path

from . import views

urlpatterns = [
    
    path('get_all_rule_template/', views.get_all_rule_template, name='get_all_rule_template'),
    path('get_rule_template/', views.get_rule_template, name='get_rule_template'),
    path('add_rule_template/', views.add_rule_template, name='add_rule_template'),
    path('update_rule_template/', views.update_rule_template, name='update_rule_template'),
    path('delete_rule_template/', views.delete_rule_template, name='delete_rule_template'),
    
    path('get_all_rule/', views.get_all_rule, name='get_all_rule'),
    path('get_rule/', views.get_rule, name='get_rule'),
    path('add_rule/', views.add_rule, name='add_rule'),
    path('update_rule/', views.update_rule, name='update_rule'),
    path('delete_rule/', views.delete_rule, name='delete_rule'),
    
    path('get_all_rule_group/', views.get_all_rule_group, name='get_all_rule_group'),
    path('get_rule_group/', views.get_rule_group, name='get_rule_group'),
    path('add_rule_group/', views.add_rule_group, name='add_rule_group'),
    path('update_rule_group/', views.update_rule_group, name='update_rule_group'),
    path('delete_rule_group/', views.delete_rule_group, name='delete_rule_group'),
    
    path('get_all_location_rule_group/', views.get_all_location_rule_group, name='get_all_location_rule_group'),
    path('get_location_rule_group/', views.get_location_rule_group, name='get_location_rule_group'),
    path('attach_rule_group_to_location/', views.attach_rule_group_to_location, name='attach_rule_group_to_location'),
    path('detach_rule_group_from_location/', views.detach_rule_group_from_location, name='detach_rule_group_from_location'),
]