
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html


# Register your models here.

# -- Edit User Admin Account display -- #
class AccountAdmin(UserAdmin):
    # -- Display some fields next to admin account name -- #
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joned' , 'is_active')
    list_display_links = ('email', 'first_name', 'last_name') # get the links to display information inside for 3 fields
    readonly_fields = ('last_login', 'date_joned') 
    ordering = ('-date_joned',) # sort following date_joned field
    
    # -- Mã hóa password -- #
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50%;">'.format(object.profile_picture.url))
    
    thumbnail.short_description = 'Profile Picture'
    
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    


admin.site.register(Account, AccountAdmin) # registor Account model
admin.site.register(UserProfile, UserProfileAdmin) # registor UserProfile