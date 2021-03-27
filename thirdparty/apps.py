"""thirdparty.apps.py"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ThirdPartyConfig(AppConfig):
    """App config."""
    name = 'thirdparty'
    verbose_name = _("Third-party")
