"""thirdparty.admin.py"""

from django.contrib import admin
from netexgl.admin import BaseModelAdmin

from .models import Company, Individual


@admin.register(Individual)
class IndividualAdmin(BaseModelAdmin):
    """Individual admin."""
    list_display = (
        'last_name',
        'first_name',
        'phone_number_1',
        'mobile_number',
        'email',
        'website',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'last_name',
        'first_name',
        'phone_number_1',
        'mobile_number',
        'email',
        'website',
    ]
@admin.register(Company)
class CompanyAdmin(BaseModelAdmin):
    """Company admin."""
    list_display = (
        'company_name',
        'phone_number_1',
        'mobile_number',
        'email',
        'website',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'company_name',
        'phone_number_1',
        'mobile_number',
        'email',
        'website',
    ]
    filter_horizontal = (
        'individuals',
    )
