"""freight.admin.py"""

from accounting.admin import (AccountingDocumentInline, CustomerBillingInline,
                              PaymentInline, SupplierBillingInline)
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from freight.models import Cargo, Docket
from netexgl.admin import BaseModelAdmin, BaseTabularInline

from .models import Cargo, Document


class CargoInline(BaseTabularInline):
    """Cargo stacked inline."""
    model = Cargo
    extra = 1
    exclude = (
        'note',
    )

class FreightDocumentInline(BaseTabularInline):
    """Document stacked inline."""
    model = Document
    verbose_name = _("Freight Document")
    verbose_name_plural = _("Freight Documents")
    extra = 1
    exclude = (
        'note',
    )


@admin.register(Docket)
class DocketAdmin(BaseModelAdmin):
    """Docket admin."""
    list_display = (
        'get_print_url',
        'docket_number_id',
        'shipper',
        'consignee',
        'invoice_completed',
        'docket_completed',
        'created_at',
        'updated_at'
    )
    list_display_links = (
        'docket_number_id',
    )
    list_filter = [
        'ready_to_invoice',
        'invoice_completed',
        'shipment_delivered',
        'docket_completed',
        'in_dispute',
        'inbond',
        'hazardous_cargo',
        'etd',
        'eta_1',
        'eta_2',
        'storage_start_date',
        'skids_exchange',
        'obl_to_shipping_line_sent',
        'obl_to_shipping_line_sent_date',
        'documents_to_broker_sent',
        'documents_to_broker_sent_date',
        'documents_to_carrier_sent',
        'documents_to_carrier_sent_date',
        'arrival_notice_received',
        'arrival_notice_received_date',
        'isf_filled',
        'isf_filled_date',
        'release_date',
        'pickup_date',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'id',
        'docket_number_id',
        'docket_type',
        'shipper_individual__first_name',
        'shipper_individual__last_name',
        'shipper_company__company_name',
        'consignee_individual__first_name',
        'consignee_individual__last_name',
        'consignee_company__company_name',
        'reference_number',
        'po_number',
        'pro_number',
        'bol_number',
        'pickup_number',
        'cc_number',
        'awb_number',
        'bl_number',
        'hbl_number',
        'cntr_number',
        'entry_number',
        'carrier__company_name'
    ]
    inlines = [
        CargoInline,
        PaymentInline,
        CustomerBillingInline,
        SupplierBillingInline,
        AccountingDocumentInline,
        FreightDocumentInline
    ]
    fieldsets = (
        (_('MAIN INFORMATION'), {
            'fields': (
                ('docket_type', 'previous_import_docket', 'previous_export_docket'),
                ('shipper_individual', 'shipper_company'),
                ('consignee_individual', 'consignee_company'),
                'note'
            )
        }),
        (_('ORIGIN ADDRESS'), {
            'classes': ('collapse',),
            'fields': (
                ('origin_address_line1', 'origin_address_line2'),
                ('origin_city_district', 'origin_state_province'),
                ('origin_postal_code', 'origin_country')
            ),
        }),
        (_('DESTINATION ADDRESS'), {
            'classes': ('collapse',),
            'fields': (
                ('destination_address_line1', 'destination_address_line2'),
                ('destination_city_district', 'destination_state_province'),
                ('destination_postal_code', 'destination_country')
            ),
        }),
        (_('STATUS'), {
            'classes': ('collapse',),
            'fields': (
                ('ready_to_invoice',
                'invoice_completed',
                'shipment_delivered',
                'docket_completed',
                'in_dispute'),
                'dispute_notes'
            ),
        }),
        (_('SHIPMENT INFORMATION'), {
            'classes': ('collapse', 'wide'),
            'fields': (
                ('inbond',
                'hazardous_cargo'),
                ('reference_number',
                'po_number'),
                ('pro_number',
                'bol_number'),
                ('pickup_number',
                'cc_number'),
                ('awb_number',
                'bl_number'),
                ('hbl_number',
                'cntr_number'),
                ('entry_number',
                'carrier'),
                'etd',
                'eta_1',
                'eta_2',
                'tracking_notes',
                'storage_start_date',
                'skids_exchange',
                'obl_to_shipping_line_sent',
                'obl_to_shipping_line_sent_date',
                'documents_to_broker_sent',
                'documents_to_broker_sent_date',
                'documents_to_carrier_sent',
                'documents_to_carrier_sent_date',
                'arrival_notice_received',
                'arrival_notice_received_date',
                'isf_filled',
                'isf_filled_date',
                'release_date',
                'pickup_date',
                'shipment_notes',
                'customer_notes'
            ),
        }),
    )
    autocomplete_fields = [
        'shipper_individual',
        'shipper_company',
        'consignee_individual',
        'consignee_company'
    ]
    readonly_fields = (
        'previous_import_docket',
        'previous_export_docket'
    )

    class Media:
        js = ("js/admin.js",)

    def previous_export_docket(self, instance): # pylint: disable=W0613,R0201
        """Get previous export docket number."""
        if Docket.objects.filter(docket_type="Export").last():
            return Docket.objects.filter(
                docket_type="Export"
            ).first().docket_number_id
        return ' - '

    def previous_import_docket(self, instance): # pylint: disable=W0613,R0201
        """Get previous import docket number."""
        if Docket.objects.filter(docket_type="Import").last():
            return Docket.objects.filter(
                docket_type="Import"
            ).first().docket_number_id
        return ' - '

    previous_export_docket.short_description = _('Previous Export Docket')
    previous_import_docket.short_description = _('Previous Import Docket')

@admin.register(Cargo)
class CargoAdmin(BaseModelAdmin):
    """Cargo admin."""
    list_select_related = (
        'docket',
    )
    list_display = (
        'description',
        'docket',
        'quantity',
        'piece_unit',
        'weight',
        'weight_unit',
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
        'description',
        'quantity',
        'piece_unit',
        'weight',
        'weight_unit',
        'length',
        'width',
        'height',
        'dimension_unit',
    ]
    autocomplete_fields = [
        'docket',
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
