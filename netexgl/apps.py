"""netexgl.apps.py"""

from django.contrib.admin.apps import AdminConfig as BaseAdminConfig


class AdminConfig(BaseAdminConfig):
    """
    Proyect adminc config.
    """
    default_site = 'netexgl.admin.AdminSite'
