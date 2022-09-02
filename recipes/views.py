from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from recipes.forms import RatingForm
from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.models import ShoppingItem
from recipes.models import Ingredient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.views.decorators.http import require_http_methods


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            try:
                rating.recipe = Recipe.objects.get(pk=recipe_id)
                rating.save()
            except Recipe.DoesNotExist:
                return redirect("recipes_list")

    return redirect("recipe_detail", pk=recipe_id)


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    paginate_by = 2


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        return context

        foods = []

        for item in self.request.user.shopping.items.all():
            foods.append(item.food_item)

        context["food_in_shopping_list"] = foods
        return context


class RecipeCreateView(CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "image"]
    success_url = reverse_lazy("recipes_list")


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "author", "description", "image"]
    success_url = reverse_lazy("recipes_list")


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "image"]
    success_url = reverse_lazy("recipes_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@require_http_methods(["POST"])
def create_shopping_item(request):
    # Get the value for the "ingredient_id" from the
    # request.POST dictionary using the "get" method

    ingredient_id = request.POST.get("ingredient_id")

    # Get the specific ingredient from the Ingredient model
    # using the code
    # Ingredient.objects.get(id=the value from the dictionary)

    ingredient = Ingredient.objects.get(id=ingredient_id)

    # Get the current user which is stored in request.user
    user = request.user

    try:
        # Create the new shopping item in the database
        # using ShoppingItem.objects.create(
        #   food_item= the food item on the ingredient,
        #   user= the current user
        # )
        ShoppingItem.objects.create(food_item=ingredient.food, user=user)

    except IntegrityError:
        pass

    return redirect("recipe_detail", pk=ingredient.recipe.id)

    # Go back to the recipe page with a redirect
    # to the name of the registered recipe detail
    # path with code like this
    # return redirect(
    #     name of the registered recipe detail path,
    #     pk=id of the ingredient's recipe
    # )


def delete_all_shopping_items(request):
    ShoppingItem.objects.filter(user=request.user).delete()
    return redirect("shopping_item_list")


class ShoppingItemListView(LoginRequiredMixin, ListView):
    model = ShoppingItem
    template_name = "shopping_items/list.html"

    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)
