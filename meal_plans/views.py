from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from meal_plans.models import MealPlan
from django.contrib.auth.mixins import LoginRequiredMixin


class MealPlansListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"
    paginate_by = 2
    # context_object_name = "Banana"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlansDetailView(LoginRequiredMixin, DetailView):
    model = MealPlan
    template_name = "meal_plans/detail.html"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["rating_form"] = RatingForm()
    #     return context


# class MealPlansCreateView(CreateView):
#     model = MealPlan
#     template_name = "meal_plans/new.html"
#     fields = ["name", "description", "image"]
#     success_url = reverse_lazy("meal_plans_list")


class MealPlansEditView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = "meal_plans/edit.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("meal_plans_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)

    def get_success_url(self) -> str:
        return reverse_lazy("meal_plans_detail", args=[self.object.id])


class MealPlansDeleteView(LoginRequiredMixin, DeleteView):
    model = MealPlan
    template_name = "meal_plans/delete.html"
    success_url = reverse_lazy("meal_plans_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlansCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = "meal_plans/new.html"
    fields = ["name", "date", "recipes"]
    success_url = reverse_lazy("meal_plans_list")

    def form_valid(self, form):
        plan = form.save(commit=False)
        plan.owner = self.request.user
        plan.save()
        form.save_m2m()
        return redirect("meal_plans_detail", pk=plan.id)
