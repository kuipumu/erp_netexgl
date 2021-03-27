"""freight.apps.py"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FreightConfig(AppConfig):
    """App config."""
    name = 'freight'
    verbose_name = _("Freight")
