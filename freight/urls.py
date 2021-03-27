"""freight.urls.py"""

from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import DocketPrintView

urlpatterns = [
    path(
        _('docket/print/<uuid:pk>'),
        DocketPrintView.as_view(),
        name='docket_print'
    )
]
