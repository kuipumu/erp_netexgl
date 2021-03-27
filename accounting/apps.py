"""accounting.apps.py"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountingConfig(AppConfig):
    """App config."""
    name = 'accounting'
    verbose_name = _("Accounting")
