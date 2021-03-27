"""accounting.admin.py"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from netexgl.admin import BaseModelAdmin, BaseTabularInline

from .models import CustomerBilling, Document, Payment, SupplierBilling


class PaymentInline(BaseTabularInline):
    """Payment stacked inline."""
    model = Payment
    extra = 1
    exclude = (
        'invoice_backup_sent',
        'invoice_backup_sent_date',
        'note'
    )

class CustomerBillingInline(BaseTabularInline):
    """CustomerBilling stacked inline."""
    model = CustomerBilling
    extra = 1
    exclude = (
        'exchange_rate',
        'invoice',
        'note'
    )
    autocomplete_fields = [
        'customer_individual',
        'customer_company'
    ]

class SupplierBillingInline(BaseTabularInline):
    """SupplierBilling stacked inline."""
    model = SupplierBilling
    extra = 1
    exclude = (
        'exchange_rate',
        'bill',
        'bill_received',
        'bill_approved',
        'bill_recorded',
        'bill_paid',
        'bill_dispute',
        'payment_date',
        'payment_type',
        'payment_scan',
        'payment_transfer_number',
        'note'
    )
    autocomplete_fields = [
        'supplier'
    ]

class AccountingDocumentInline(BaseTabularInline):
    """Document stacked inline."""
    model = Document
    verbose_name = _("Accounting Document")
    verbose_name_plural = _("Accounting Documents")
    extra = 1
    exclude = (
        'note',
    )

@admin.register(Payment)
class PaymentAdmin(BaseModelAdmin):
    """Payment admin."""
    list_select_related = (
        'docket',
    )
    list_display = (
        'invoice_no',
        'payment_type',
        'payment_transfer_number',
        'payment_date',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'payment_type',
        'payment_date',
        'invoice_backup_sent',
        'invoice_backup_sent_date',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'id',
        'docket__docket_number_id',
        'invoice_no',
        'payment_type',
        'payment_transfer_number',
        'payment_date'
    ]
    autocomplete_fields = [
        'docket',
    ]

@admin.register(CustomerBilling)
class CustomerBillingAdmin(BaseModelAdmin):
    """CustomerBilling admin."""
    list_select_related = (
        'docket',
    )
    list_display = (
        'customer',
        'customer_service',
        'bill_to',
        'price',
        'currency',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'bill_to',
        'customer_service',
        'currency',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'id',
        'docket__docket_number_id',
        'bill_to',
        'customer_individual__first_name',
        'customer_individual__last_name',
        'customer_company__company_name',
        'customer_service',
        'price',
        'currency'
    ]
    autocomplete_fields = [
        'docket',
        'customer_individual',
        'customer_company'
    ]

@admin.register(SupplierBilling)
class SupplierBillingAdmin(BaseModelAdmin):
    """SupplierBilling admin."""
    list_select_related = (
        'docket',
    )
    list_display = (
        'supplier',
        'supplier_service',
        'bill_to',
        'price',
        'currency',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'bill_to',
        'supplier_service',
        'currency',
        'bill_received',
        'bill_approved',
        'bill_recorded',
        'bill_paid',
        'bill_dispute',
        'payment_type',
        'payment_date',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'id',
        'docket__docket_number_id',
        'bill_to',
        'supplier__company_name',
        'supplier_service',
        'price',
        'currency'
    ]
    autocomplete_fields = [
        'docket',
        'supplier',
    ]

@admin.register(Document)
class DocumentAdmin(BaseModelAdmin):
    """Document admin."""
    list_select_related = (
        'docket',
    )
    list_display = (
        'name',
        'description',
        'docket',
        'file',
        'created_at',
        'updated_at'
    )
    list_filter = [
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'id',
        'docket__docket_number_id',
        'name',
        'description',
    ]
