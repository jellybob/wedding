from django.contrib import admin
from wedding.gifts.models import Gift, Category

class GiftAdmin(admin.ModelAdmin):
    list_display = ("name", "price_in_pounds", "reserved")
    prepopulated_fields = { "slug": ("name",) }
    list_filter = ("reserved",)
admin.site.register(Gift, GiftAdmin)

admin.site.register(Category)