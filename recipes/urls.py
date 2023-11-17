from django.urls import path
from django.views.decorators.cache import cache_page

from recipes.views import RecipeHome, RecipeAll, RecipeUser, RecipeAdd, Contact, LoginUser, logout_user, RegisterUser, \
    RecipeCatAll, RecipeCatUser, RecipeShow, RecipeEdit, ProfileEdit, redirect_to_instagram, redirect_to_telegram


urlpatterns = [
    path('', RecipeHome.as_view(), name='home'),
    path('all/',RecipeAll.as_view(), name='all'),
    path('user/', RecipeUser.as_view(), name='user'),
    path('addrecipe/', RecipeAdd.as_view(), name='add_recipe'),
    path('contact/',cache_page(60)(Contact.as_view()), name='contact'),
    path('login/',cache_page(60)(LoginUser.as_view()), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',cache_page(60)(RegisterUser.as_view()), name='register'),
    path('all/category/<slug:cat_slug>/', RecipeCatAll.as_view(), name='category_all'),
    path('user/category/<slug:cat_slug>/', RecipeCatUser.as_view(), name='category_user'),
    path('recipe/<slug:recipe_slug>/', RecipeShow.as_view(), name='recipe'),
    path('recipe/edit/<slug:recipe_slug>/', RecipeEdit.as_view(), name='edit_recipe'),
    path('profile/edit/<int:user_id>/',ProfileEdit.as_view(), name='edit_profile'),
    path('redirect_instagram/', redirect_to_instagram, name='redirect_instagram'),
    path('redirect_telegram/', redirect_to_telegram, name='redirect_telegram'),
]
