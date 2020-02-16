from django.contrib import admin
from django.db import models
from .models import Player, Level, GameObject
from martor.widgets import AdminMartorWidget


class PlayerModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class LevelModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


class GameObjectModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


# Register your models here.
admin.site.register(Player, PlayerModelAdmin)
admin.site.register(Level, LevelModelAdmin)
admin.site.register(GameObject, GameObjectModelAdmin)