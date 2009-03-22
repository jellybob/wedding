from django.contrib import admin
from wedding.guests.models import Guest, GuestGroup

class GuestAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'), 
                       'email', 
                       'phone', 
                       'address', 
                       'group', 
                       ('invite_to_meal', 'save_the_date_sent', 'invite_sent'),
                       ('attending_ceremony', 'attending_meal', 'attending_reception'))
        }),
    )
    
    list_display = ('first_name', 'last_name', 'group', 'save_the_date_sent', 'invite_sent', 'invite_to_meal',
                    'attending_ceremony', 'attending_meal', 'attending_reception')
    list_filter = ('group', 'save_the_date_sent', 'invite_sent', 'invite_to_meal', 
                   'attending_ceremony', 'attending_meal', 'attending_reception')
    ordering = ['last_name']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
admin.site.register(Guest, GuestAdmin)

class GuestGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(GuestGroup, GuestGroupAdmin)