from django.contrib import admin
from wedding.gifts.models import Gift

class GiftAdmin(admin.ModelAdmin):
    prepopulated_fields = { "slug": ("name",) }
admin.site.register(Gift, GiftAdmin)