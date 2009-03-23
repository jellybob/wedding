from django.contrib import admin
from wedding.guests.models import Guest, Group, Category

class GuestInline(admin.TabularInline):
    model = Guest
    
class GroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'address', 'category', 'invite_to_meal', 
                       ('save_the_date_sent', 'invite_sent', 'rsvp_received'))
        }),
    )
    
    inlines = [GuestInline]
    
    list_display = ('name', 'email', 'category', 'invite_to_meal', 'save_the_date_sent', 'invite_sent', 'rsvp_received')
    list_filter = ('category', 'invite_to_meal', 'save_the_date_sent', 'invite_sent', 'rsvp_received')
    search_fields = ['name', 'email', 'phone', 'address']
admin.site.register(Group, GroupAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)
