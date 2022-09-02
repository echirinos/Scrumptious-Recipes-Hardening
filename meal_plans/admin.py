from django.contrib import admin

from meal_plans.models import MealPlan


class MealPlanAdmin(admin.ModelAdmin):
    pass


admin.site.register(MealPlan, MealPlanAdmin)
