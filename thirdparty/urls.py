"""thirdparty.urls.py"""

from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .views import CompanyAddressView, IndividualAddressView

urlpatterns = [
    path(
        _('individual/ajax/address'),
        IndividualAddressView.as_view(),
        name='ajax_individual_address'
    ),
    path(
        _('company/ajax/address'),
        CompanyAddressView.as_view(),
        name='ajax_company_address'
    ),
]
