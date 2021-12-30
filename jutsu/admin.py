from django.contrib import admin
from .models import Jutsu
from .models import Enhancement


class EnhancementInline(admin.StackedInline):
    model = Enhancement
    extra = 1


class JutsuAdmin(admin.ModelAdmin):
    inlines = [
        EnhancementInline,
    ]


admin.site.register(Jutsu, JutsuAdmin)
admin.site.register(Enhancement)