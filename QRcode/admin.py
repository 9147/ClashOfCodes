from django.contrib import admin
from .models import DemoUser, CurrentFoodCheck

@admin.register(DemoUser)
class DemoUserAdmin(admin.ModelAdmin):
    list_display = ('name','id','unique_code', 'role', 'team_name', 'lunch1', 'dinner', 'breakfast', 'lunch2', 'lunch1_completed', 'dinner_completed', 'breakfast_completed', 'lunch2_completed')
    search_fields = ('name', 'role', 'team_name')

@admin.register(CurrentFoodCheck)
class CurrentFoodCheckAdmin(admin.ModelAdmin):
    list_display = ('current_food',)