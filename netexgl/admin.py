"""netexgl.admin.py"""

from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from reversion.admin import VersionAdmin

from .settings import SITE_HEADER, SITE_TITLE


class AdminSite(admin.AdminSite):
    """Main admin site."""
    site_header = SITE_HEADER
    site_title = SITE_TITLE
    site_url = None
    enable_nav_sidebar = False

    def index(self, request, extra_context=None):
        """Index method."""
        if extra_context is None:
            extra_context = {}

        # Sort the apps alphabetically.
        app_list = self.get_app_list(request)
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        extra_context['app_list'] = app_list
        return super().index(request, extra_context)

class BaseModelAdmin(VersionAdmin, admin.ModelAdmin):
    """Base ModelAdmin."""
    date_hierarchy = 'created_at'

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Get form method."""
        form = super().get_form(request, obj, **kwargs)
        # Reorder abstract model fields to go bottom.
        if 'note' in form.base_fields:
            note = form.base_fields.pop('note')
            form.base_fields['note'] = note
        return form

class BaseTabularInline(admin.TabularInline):
    """Base TabularInline."""
    formfield_overrides = {
        PhoneNumberField: {'widget': PhoneNumberInternationalFallbackWidget},
    }

    classes= [
        'collapse'
    ]
    show_change_link = True
