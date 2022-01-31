from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('', lambda req: redirect('/pokedex/accueil')),
    path('admin/', admin.site.urls),
    path('pokedex/', include('pokedex.urls')),
]
