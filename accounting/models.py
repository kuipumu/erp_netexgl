"""accounting.models.py"""

from pathlib import PurePath

from accounting.data import (BILL_TO_N, CURRENCY_TYPES, PAYMENT_TYPES,
                             SUPPLIER_AND_CUSTOMER_SERVICES)
from django.contrib.postgres.fields import CICharField
from django.db.models import (CASCADE, PROTECT, BooleanField, DateField,
                              DateTimeField, DecimalField, FileField,
                              ForeignKey, PositiveIntegerField, UUIDField)
from django.utils.translation import ugettext_lazy as _
from freight.models import Docket
from netexgl.models import BaseModel
from thirdparty.models import Company, Individual


class Payment(BaseModel):
    """Define the payment model."""
    docket = ForeignKey(
        Docket,
        on_delete=CASCADE,
        blank=False,
        null=False
    )
    payment_type = CICharField(
        _('Type'),
        max_length=150,
        choices=PAYMENT_TYPES,
        blank=True,
        null=True,
    )
    payment_transfer_number = CICharField(
        _('Transfer Number'),
        max_length=250,
        blank=True,
        null=True,
    )
    payment_date = DateField(
        _('Payment Date'),
        blank=True,
        null=True
    )
    invoice_no = CICharField(
        _('Invoice #'),
        max_length=250,
        blank=False,
        null=False,
    )
    invoice_backup_sent = BooleanField(
        _('Invoice Backup'),
        default=False,
    )
    invoice_backup_sent_date = DateField(
        _('Invoice Backup Sent Date'),
        blank=True,
        null=True
    )
    payment_scan = FileField(
        _('Scan'),
        blank=True,
        null=True,
        upload_to='uploads/payment_details/payment_scans/%Y/%m/%d/'
    )

    def __str__(self):
        return str(self.id)


class CustomerBilling(BaseModel):
    """Define customer billing model."""
    docket = ForeignKey(
        Docket,
        on_delete=CASCADE,
        blank=False,
        null=False
    )
    bill_to = CICharField(
        _('BT #'),
        max_length=100,
        choices=BILL_TO_N,
        blank=False,
        null=False,
    )
    customer_company = ForeignKey(
        Company,
        verbose_name=_('Company'),
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    customer_individual = ForeignKey(
        Individual,
        verbose_name=_('Individual'),
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    customer_service = CICharField(
        _('Service'),
        max_length=150,
        choices=SUPPLIER_AND_CUSTOMER_SERVICES,
        blank=False,
        null=False,
    )
    price = DecimalField(
        _('Price'),
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True
    )
    currency = CICharField(
        _('Currency'),
        max_length=10,
        choices=CURRENCY_TYPES,
        blank=False,
        null=False,
    )
    exchange_rate = PositiveIntegerField(
        _('Exchange Rate'),
        blank=True,
        null=True
    )
    invoice = FileField(
        _('Invoice'),
        blank=True,
        null=True,
        upload_to='uploads/bills/customer/invoices/%Y/%m/%d/'
    )
    invoice_no = CICharField(
        _('Invoice #'),
        max_length=250,
        blank=True,
        null=True,
    )

    class Meta:
        """Model meta."""
        verbose_name = _('billing (customer)')
        verbose_name_plural = _('billings (customer)')

    def customer(self):
        """
        Get actual customer.
        """
        if self.customer_individual is not None:
            return self.customer_individual
        return self.customer_company

    def __str__(self):
        return str(self.id)


class SupplierBilling(BaseModel):
    """Define supplier billing model."""
    docket = ForeignKey(
        Docket,
        on_delete=CASCADE,
        blank=False,
        null=False
    )
    bill_to = CICharField(
        _('BT #'),
        max_length=100,
        choices=BILL_TO_N,
        blank=False,
        null=False,
    )
    supplier = ForeignKey(
        Company,
        verbose_name=_('Supplier'),
        on_delete=PROTECT,
        blank=True,
        null=True,
    )
    supplier_service = CICharField(
        _('Service'),
        max_length=150,
        choices=SUPPLIER_AND_CUSTOMER_SERVICES,
        blank=False,
        null=False,
    )
    price = DecimalField(
        _('Price'),
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True
    )
    currency = CICharField(
        _('Currency'),
        max_length=10,
        choices=CURRENCY_TYPES,
        blank=False,
        null=False,
    )
    exchange_rate = PositiveIntegerField(
        _('XR'),
        blank=True,
        null=True
    )
    bill_no = CICharField(
        _('Bill #'),
        max_length=250,
        blank=True,
        null=True,
    )
    bill = FileField(
        _('Bill'),
        blank=True,
        null=True,
        upload_to='uploads/bills/supplier/%Y/%m/%d/'
    )
    bill_received = BooleanField(
        _('Received'),
        default=False
    )
    bill_approved = BooleanField(
        _('Approved'),
        default=False
    )
    bill_recorded = BooleanField(
        _('Recorded'),
        default=False
    )
    bill_paid = BooleanField(
        _('Paid'),
        default=False
    )
    bill_dispute = BooleanField(
        _('Dispute'),
        default=False
    )
    payment_date = DateField(
        _('Payment Date'),
        blank=True,
        null=True
    )
    payment_type = CICharField(
        _('Payment Type'),
        max_length=150,
        choices=PAYMENT_TYPES,
        blank=True,
        null=True,
    )
    payment_scan = FileField(
        _('Payment Scan'),
        blank=True,
        null=True,
        upload_to='uploads/bills/supplier/payment_scans/%Y/%m/%d/'
    )
    payment_transfer_number = CICharField(
        _('Transfer #'),
        max_length=250,
        blank=True,
        null=True,
    )

    class Meta:
        """Model meta."""
        verbose_name = _('billing (supplier)')
        verbose_name_plural = _('billings (supplier)')

    def __str__(self):
        return str(self.id)

class Document(BaseModel):
    """Define document model."""
    docket = ForeignKey(
        Docket,
        related_name='accounting_document_docket',
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
