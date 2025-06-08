from django.contrib import admin
from .models import Place, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('title', 'address')
    search_fields = ('title', 'address')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating')
    search_fields = ('place__title', 'user__username')
