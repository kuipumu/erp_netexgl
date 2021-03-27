"""thirdparty.views.py"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import View

from .models import Company, Individual


class IndividualAddressView(LoginRequiredMixin, View):
    """View to get individual address on JSON."""
    login_url = 'login'

    def get(self, request):
        """GET method."""
        query = self.request.GET.get('q')
        if query:
            obj = Individual.objects.get(id=query)
            data = {
                'address_line1': obj.address_line1,
                'address_line2': obj.address_line2,
                'city_district': obj.city_district,
                'state_province': obj.state_province,
                'postal_code': obj.postal_code,
                'country': obj.country,
            }
            return JsonResponse(data)
        return HttpResponse('')


class CompanyAddressView(LoginRequiredMixin, View):
    """View to get company address on JSON."""
    login_url = 'login'

    def get(self, request):
        """GET method."""
        query = self.request.GET.get('q')
        if query:
            obj = Company.objects.get(id=query)
            data = {
                'address_line1': obj.address_line1,
                'address_line2': obj.address_line2,
                'city_district': obj.city_district,
                'state_province': obj.state_province,
                'postal_code': obj.postal_code,
                'country': obj.country,
            }
            return JsonResponse(data)
        return HttpResponse('')
