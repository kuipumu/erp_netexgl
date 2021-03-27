"""freight.models.py"""

from pathlib import PurePath

from django.contrib.postgres.fields import CICharField, CITextField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, PROTECT, BooleanField, DateField,
                              DateTimeField, FileField, FloatField, ForeignKey,
                              PositiveIntegerField)
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from freight.data import (DIMENSION_UNITS, DOCKET_TYPES, UNIT_TYPES,
                          WEIGHT_UNITS)
from netexgl.data import COUNTRIES
from netexgl.models import BaseModel
from thirdparty.models import Company, Individual

from .settings import (DOCKET_EXPORT_INITIAL, DOCKET_EXPORT_PREFIX,
                       DOCKET_IMPORT_INITIAL, DOCKET_IMPORT_PREFIX)


def get_docket_number_id(first, prefix, initial):
    """Function to generate docket number id."""
    # Check if there is a item on queryset.
    if first:
        # Get docket number from last item.
        docket_number = int(''.join(
            filter(
                str.isdigit, first.docket_number_id
                )
            )
        )
        # Increment docket number.
        object_number = docket_number + 1
        # Return number with prefix.
        return str(prefix) + '-' + str(object_number)
    # Increment initial docket number.
    object_number = int(initial) + 1
    # Return number with prefix.
    return str(prefix) + '-' + str(object_number)


class Docket(BaseModel):
    """Define docket model."""
    docket_number_id = CICharField(
        _('Docket #'),
        help_text=_('The current docket identification number ID.'),
        max_length=250,
        blank=False,
        null=False,
        unique=True,
        editable=False
    )
    docket_type = CICharField(
        _('Type'),
        max_length=60,
        choices=DOCKET_TYPES,
        blank=False,
        null=False,
    )
    shipper_individual = ForeignKey(
        Individual,
        on_delete=PROTECT,
        verbose_name=_('Shipper Individual'),
        related_name='docket_ca_shipper_individual',
        blank=True,
        null=True
    )
    shipper_company = ForeignKey(
        Company,
        on_delete=PROTECT,
        verbose_name=_('Shipper Company'),
        related_name='docket_ca_shipper_company',
        blank=True,
        null=True
    )
    consignee_individual = ForeignKey(
        Individual,
        on_delete=PROTECT,
        verbose_name=_('Consignee Individual'),
        related_name='docket_ca_consignee_individual',
        blank=True,
        null=True
    )
    consignee_company = ForeignKey(
        Company,
        on_delete=PROTECT,
        verbose_name=_('Consignee Company'),
        related_name='docket_ca_consignee_company',
        blank=True,
        null=True
    )
    # Origin Address
    origin_address_line1 = CICharField(
        _('Address Line 1'),
        max_length=255,
        blank=False,
        null=False,
    )
    origin_address_line2 = CICharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        null=True,
    )
    origin_city_district = CICharField(
        _('City / District'),
        max_length=255,
        blank=False,
        null=False,
    )
    origin_state_province = CICharField(
        _('State / Province'),
        max_length=255,
        blank=False,
        null=False,
    )
    origin_postal_code = CICharField(
        _('ZIP C. / Postal C. '),
        max_length=50,
        blank=False,
        null=False,
    )
    origin_country = CICharField(
        _('Country'),
        max_length=150,
        choices=COUNTRIES,
        blank=False,
        null=False,
    )
    # Destination Address
    destination_address_line1 = CICharField(
        _('Address Line 1'),
        max_length=255,
        blank=False,
        null=False,
    )
    destination_address_line2 = CICharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        null=True,
    )
    destination_city_district = CICharField(
        _('City / District'),
        max_length=255,
        blank=False,
        null=False,
    )
    destination_state_province = CICharField(
        _('State / Province'),
        max_length=255,
        blank=False,
        null=False,
    )
    destination_postal_code = CICharField(
        _('ZIP C. / Postal C. '),
        max_length=50,
        blank=False,
        null=False,
    )
    destination_country = CICharField(
        _('Country'),
        max_length=150,
        choices=COUNTRIES,
        blank=False,
        null=False,
    )
    # Shipment Information.
    inbond = BooleanField(
        _('Inbond'),
        default=False
    )
    hazardous_cargo = BooleanField(
        _('Hazardous Cargo'),
        default=False
    )
    reference_number = CICharField(
        _('REF No. #'),
        help_text=_('Reference Number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    po_number = CICharField(
        _('PO No. #'),
        help_text=_('Purchase order Number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    pro_number = CICharField(
        _('PRO No. #'),
        help_text=_('Progressive Number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    bol_number = CICharField(
        _('BOL No. #'),
        help_text=_('Bill of lading Number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    pickup_number = CICharField(
        _('Pickup No. #'),
        help_text=_('Pickup number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    cc_number = CICharField(
        _('CC No. #'),
        help_text=_('Cargo control number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    awb_number = CICharField(
        _('AWB No. #'),
        help_text=_('Air waybill number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    bl_number = CICharField(
        _('BL No. #'),
        help_text=_('BL number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    hbl_number = CICharField(
        _('HBL No. #'),
        help_text=_('House bill of lading number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    cntr_number = CICharField(
        _('CNTR No. #'),
        help_text=_('Container Number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    entry_number = CICharField(
        _('Entry No. #'),
        help_text=_('Entry number of the docket.'),
        max_length=100,
        blank=True,
        null=True,
    )
    carrier = ForeignKey(
        Company,
        on_delete=PROTECT,
        verbose_name=_('carrier'),
        related_name='docket_ca_carrier',
        blank=True,
        null=True
    )
    etd = DateField(
        _('Est. Time of Delivery'),
        blank=True,
        null=True
    )
    eta_1 = DateField(
        _('Est. Time of Arrival 1'),
        blank=True,
        null=True
    )
    eta_2 = DateField(
        _('Est. Time of Arrival 2'),
        blank=True,
        null=True
    )
    tracking_notes = CITextField(
        _('Tracking Note'),
        blank=True,
        null=True
    )
    storage_start_date = DateField(
        _('Storage Start Date'),
        blank=True,
        null=True
    )
    skids_exchange = BooleanField(
        _('Skids Exchange'),
        default=False
    )
    obl_to_shipping_line_sent = BooleanField(
        _('OBL To Shipping Line Sent'),
        default=False
    )
    obl_to_shipping_line_sent_date = DateField(
        _('OBL To Shipping Line Sent Date'),
        blank=True,
        null=True
    )
    documents_to_broker_sent = BooleanField(
        _('Documents To Broker Sent'),
        default=False
    )
    documents_to_broker_sent_date = DateField(
        _('Documents To Broker Sent Date'),
        blank=True,
        null=True
    )
    documents_to_carrier_sent = BooleanField(
        _('Documents To Carrier Sent'),
        default=False
    )
    documents_to_carrier_sent_date = DateField(
        _('Documents To Carrier Sent Date'),
        blank=True,
        null=True
    )
    arrival_notice_received = BooleanField(
        _('Arrival Notice Received'),
        default=False
    )
    arrival_notice_received_date = DateField(
        _('Arrival Notice Received Date'),
        blank=True,
        null=True
    )
    isf_filled = BooleanField(
        _('ISF Filled'),
        default=False
    )
    isf_filled_date = DateField(
        _('ISF Filled Date'),
        blank=True,
        null=True
    )
    release_date = DateField(
        _('Release Date'),
        blank=True,
        null=True
    )
    pickup_date = DateField(
        _('Pickup Date'),
        blank=True,
        null=True
    )
    shipment_notes = CITextField(
        _('Shipment Note'),
        help_text=_('Shipment note of the docket (only for employees.).'),
        blank=True,
        null=True
    )
    customer_notes = CITextField(
        _('Customer Note'),
        help_text=_('Customer note of the docket (only for client).'),
        blank=True,
        null=True
    )
    # Status
    ready_to_invoice = BooleanField(
        _('Ready To Invoice'),
        default=False
    )
    invoice_completed = BooleanField(
        _('Invoice Completed'),
        default=False
    )
    shipment_delivered = BooleanField(
        _('Shipment Delivered'),
        default=False
    )
    docket_completed = BooleanField(
        _('Docket Completed'),
        default=False
    )
    in_dispute = BooleanField(
        _('In Dispute'),
        default=False
    )
    dispute_notes = CITextField(
        _('Dispute Note'),
        help_text=_('Dispute note of the docket.'),
        blank=True,
        null=True
    )

    def get_print_url(self):
        '''
        Returns print URL of model.
        '''
        return format_html(
            '<a href="{}" target="_blank">\
            <img src="/static/admin/img/icon-viewlink.svg" alt="View">\
            </a>',
            reverse_lazy('docket_print', args=[str(self.id)]),
        )
    get_print_url.short_description = _('Print')

    def shipper(self):
        """Get shipper."""
        if self.shipper_individual is not None:
            return self.shipper_individual
        return self.shipper_company

    def consignee(self):
        """Get consignee."""
        if self.consignee_individual is not None:
            return self.consignee_individual
        return self.consignee_company

    def clean(self):
        """Clean method."""
        # Check that only one shipper type can be set.
        if not self.shipper_individual and not self.shipper_company:
            raise ValidationError(_('Shipper must be set.'))
        # Check that only one consignee type can be set.
        if not self.consignee_individual and not self.consignee_company:
            raise ValidationError(_('Consignee must be set.'))
        # Check that only one shipper type is set.
        if self.shipper_individual and self.shipper_company:
            raise ValidationError(_('Only one shipper type can be set.'))
        # Check that only one consignee type is set.
        if self.consignee_individual and self.consignee_company:
            raise ValidationError(_('Only one consignee type can be set.'))
        # Check if no docket number has been set.
        if not self.docket_number_id:
            # Create Docket Number for export docket.
            if self.docket_type == 'Export':
                docket_number = get_docket_number_id(
                    Docket.objects.filter(docket_type='Export').first(),
                    DOCKET_EXPORT_PREFIX,
                    DOCKET_EXPORT_INITIAL
                )
                self.docket_number_id = docket_number
            # Create Docket Number for import docket.
            if self.docket_type == "Import":
                # Remove delete from previous docket.
                docket_number = get_docket_number_id(
                    Docket.objects.filter(docket_type='Import').first(),
                    DOCKET_IMPORT_PREFIX,
                    DOCKET_IMPORT_INITIAL
                )
                self.docket_number_id = docket_number

    def __str__(self):
        return str(self.docket_number_id)


class Cargo(BaseModel):
    """Define cargo model."""
    docket = ForeignKey(
        Docket,
        verbose_name=_('Docket'),
        on_delete=CASCADE,
        blank=False,
        null=False
    )
    description = CICharField(
        _('Description'),
        max_length=250,
        blank=True,
        null=True
    )
    quantity = PositiveIntegerField(
        _('Quantity'),
        blank=False,
        null=False,
    )
    piece_unit = CICharField(
        _('Piece Unit'),
        max_length=80,
        choices=UNIT_TYPES,
        blank=False,
        null=False,
    )
    weight = FloatField(
        _('Weight'),
        validators=[MinValueValidator(0)],
        blank=False,
        null=False,
    )
    weight_unit = CICharField(
        _('Weight Unit'),
        max_length=80,
        choices=WEIGHT_UNITS,
        blank=True,
        null=True,
    )
    length = FloatField(
        _('Length'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    width = FloatField(
        _('Width'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    height = FloatField(
        _('Height'),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    dimension_unit = CICharField(
        _('Dimension Unit'),
        max_length=80,
        choices=DIMENSION_UNITS,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.description)

class Document(BaseModel):
    """Define document model."""
    docket = ForeignKey(
        Docket,
        verbose_name=_('Docket'),
        related_name='freight_document_docket',
        on_delete=CASCADE,
        blank=True,
        null=True
    )
    name = CICharField(
        _('Name'),
        max_length=250,
        blank=False,
        null=False
    )
    description = CICharField(
        _('Description'),
        max_length=250,
        blank=True,
        null=True
    )
    file = FileField(
        _('Document'),
        blank=False,
        null=False,
        upload_to='uploads/documents/%Y/%m/%d/'
    )

    def filename(self):
        """Get filename from document."""
        return PurePath.name(self.file.name)

    def __str__(self):
        return str(self.name)
