from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddRecipeForm, UpdateProfileForm, ContactForm, RegisterUserForm, LoginUserForm
from .models import Recipe, Category
from .utils import DataMixin


class RecipeHome(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Recipe.objects.order_by('?')[:5].select_related('author').prefetch_related('cat')


class RecipeUser(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/user.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои рецепты", author_id=self.request.user.id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        _author_id = self.request.user.id
        return Recipe.objects.filter(author_id=_author_id).select_related('author').prefetch_related('cat')


class RecipeAll(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Все рецепты")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Recipe.objects.order_by('?').select_related('author').prefetch_related('cat')


class RecipeAdd(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddRecipeForm
    template_name = 'recipes/addrecipe.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить рецепт")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.instance.author = self.request.user
        instance = form.save(commit=False)
        filename = instance.photo.name.split('/')[-1]
        new_filename = filename.split('.')[0] + '.png'
        instance.photo.path.replace(filename, new_filename)
        instance.photo.name = new_filename
        return super().form_valid(form)


class RecipeEdit(DataMixin, UpdateView):
    form_class = AddRecipeForm
    model = Recipe
    template_name = 'recipes/editrecipe.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True
    slug_url_kwarg = "recipe_slug"


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование рецепта")
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfileEdit(DataMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'recipes/editprofile.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_object(self):
        id_ = self.kwargs.get('user_id')
        return get_object_or_404(User, id=id_)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование профиля")
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        return super().form_valid(form)


class RecipeShow(DataMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    slug_url_kwarg = 'recipe_slug'
    context_object_name = 'recipe'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['recipe'])
        return dict(list(context.items()) + list(c_def.items()))


class RecipeCatAll(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes.html'
    context_object_name = 'recipes'
    allow_empty = False

    def get_queryset(self):
        return Recipe.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('author').prefetch_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Все рецепты - Категория - ' + str(c.name),
            cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RecipeCatUser(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/user.html'
    context_object_name = 'recipes'
    allow_empty = False

    def get_queryset(self):
        return Recipe.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True, author_id=self.request.user.id).select_related('author').prefetch_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Мои рецепты - Категория - ' + str(c.name),
            cat_selected=c.pk, author_id=self.request.user.id)
        return dict(list(context.items()) + list(c_def.items()))


class Contact(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'recipes/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'recipes/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'recipes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def redirect_to_instagram(request):
    return redirect("https://www.instagram.com/keepcalmaboss")


def redirect_to_telegram(request):
    return redirect("https://t.me/keepcalmaboss")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')