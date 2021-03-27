"""freight.views.py"""

import io
from datetime import datetime

from accounting.models import CustomerBilling, Payment, SupplierBilling
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from thirdparty.models import Individual

from .models import Cargo, Docket


class DocketPrintView(LoginRequiredMixin, View):
    '''
    View to create a PDF information using a Generic View.
    '''
    login_url = 'login'

    def get(self, request, pk):
        """
        Get method for PDF view.
        """

        obj = Docket.objects.get(id=pk)
        buff = io.BytesIO()
        doc = SimpleDocTemplate(
            buff,
            pagesize=landscape(letter),
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm,
        )

        styles = getSampleStyleSheet()
        styles['Normal'].fontSize = 10
        content = []

        # Function to print a date.
        def date_table(date):
            if date is None:
                return ''
            return Paragraph(str(date), styles['Normal'])

        # Function to print a boolean.
        def bool_table(boolean):
            if boolean is True:
                return Paragraph('Yes', styles['Normal'])
            if boolean is None:
                return Paragraph('No', styles['Normal'])
            return None

        # Function to print a string.
        def string_table(string):
            if string is not None:
                return Paragraph(str(string), styles['Normal'])
            if string is None:
                return Paragraph('', styles['Normal'])
            return None

        # Header
        header_title = Paragraph(
            str(_('Docket')) + ' ' + str(_('Report')) + ' - ' \
            + str(obj.docket_number_id) ,
            styles['Heading1']
        )
        report_info = str(_(
            'Report Date:'
            )) + ' ' + str(
            datetime.now().strftime("%x %X")
            )
        report_info = Paragraph(report_info, styles['Normal'])
        header = [
            [header_title, report_info],
        ]
        header_table = Table(
            header,
            colWidths=(19.8*cm, 5.8*cm),
            hAlign='LEFT'
        )
        header_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
                ('BOX', (0, 0), (-1, -1), 0, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]
        ))

        # Origin and Destination.
        if obj.shipper_individual is None and obj.shipper_company is not None:
            shipper = Paragraph(
                str(obj.shipper_company.company_name), styles["Normal"]
            )
        elif obj.shipper_company is None and \
                obj.shipper_individual is not None:
            consignee = Paragraph(
                str(obj.shipper_individual.get_full_name()), styles["Normal"]
            )
        elif obj.shipper_individual is None and obj.shipper_company is None:
            shipper = Paragraph('', styles["Normal"])

        if obj.consignee_individual is None and \
                obj.consignee_company is not None:
            consignee = Paragraph(
                str(obj.consignee_company.company_name), styles["Normal"]
            )
        elif obj.consignee_company is None and \
                obj.consignee_individual is not None:
            consignee = Paragraph(
                str(obj.consignee_individual.get_full_name()), styles["Normal"]
            )
        elif obj.consignee_individual is None and \
                obj.consignee_company is None:
            consignee = Paragraph('', styles["Normal"])

        if obj.origin_address_line2 is None:
            origin = str(obj.origin_address_line1) + ', ' \
                + str(obj.origin_city_district) + ', ' \
                + str(obj.origin_state_province) + ', ' \
                + str(obj.origin_country) + ', '  \
                + str(obj.origin_postal_code)
        else:
            origin = str(obj.origin_address_line1) + ', ' \
                + str(obj.origin_address_line2) + ', ' \
                + str(obj.origin_city_district) + ', ' \
                + str(obj.origin_state_province) + ', ' \
                + str(obj.origin_country) + ', '  \
                + str(obj.origin_postal_code)

        if obj.destination_address_line2 is None:
            destination = str(obj.destination_address_line1) + ', ' \
                + str(obj.destination_city_district) + ', ' \
                + str(obj.destination_state_province) + ', ' \
                + str(obj.destination_country) + ', '  \
                + str(obj.destination_postal_code)
        else:
            destination = str(obj.destination_address_line1) + ', ' \
                + str(obj.destination_address_line2) + ', ' \
                + str(obj.destination_city_district) + ', ' \
                + str(obj.destination_state_province) + ', ' \
                + str(obj.destination_country) + ', '  \
                + str(obj.destination_postal_code)
        origin_destination = [
            [Paragraph(
                _('Origin'),
                styles['Normal']),
                Paragraph(str(origin), styles["Normal"])],
            [Paragraph(
                _('Destination'),
                styles['Normal']),
                Paragraph(str(destination), styles["Normal"])]
        ]
        origin_destination_table = Table(
            origin_destination,
            colWidths=(4*cm, 6.5*cm),
            minRowHeights=(1.8*cm, 1.8*cm),
            hAlign='LEFT'
        )
        origin_destination_table.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))

        # Docket Information.
        docket_information = [
            [Paragraph(_('Docket #'), styles['Normal']),
                Paragraph(str(obj.docket_number_id), styles['Normal']),
                Paragraph(_('Ready To Invoice'), styles['Normal']),
                bool_table(obj.ready_to_invoice)],

            [Paragraph(_('Type of Docket'), styles['Normal']),
                Paragraph(str(obj.docket_type), styles['Normal']),
                Paragraph(_('Shipment Delivered'), styles['Normal']),
                bool_table(obj.shipment_delivered)],

            [Paragraph(_('Consignee'), styles['Normal']), consignee,
                Paragraph(_('Invoice Completed'), styles['Normal']),
                bool_table(obj.invoice_completed)],

            [Paragraph(_('Shipper'), styles['Normal']), shipper,
                Paragraph(_('Docket Completed'), styles['Normal']),
                bool_table(obj.docket_completed)],

            [Paragraph(_('ID'), styles['Normal']),
                Paragraph(str(obj.id), styles['Normal']),
                Paragraph(_('In Dispute'), styles['Normal']),
                bool_table(obj.in_dispute)],

        ]
        docket_information_table = Table(
            docket_information,
            colWidths=(4*cm, 5*cm, 4*cm, 1.2*cm),
            hAlign='LEFT',
        )
        docket_information_table.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))

        # Docket Top Row.
        top_row = [
            [docket_information_table, origin_destination_table],
        ]
        top_row_table = Table(
            top_row,
            hAlign='LEFT',
            longTableOptimize=True,
        )
        top_row_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
                ('BOX', (0, 0), (-1, -1), 0, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))

        # Shipment Information.
        shipment_information_header = Paragraph(
            _('Shipment Information'), styles['Heading2']
        )
        shipment_information_a = [
            [Paragraph(_('PO #'), styles['Normal']),
                string_table(obj.po_number)],

            [Paragraph(_('PRO #'), styles['Normal']),
                string_table(obj.pro_number)],

            [Paragraph(_('BOL #'), styles['Normal']),
                string_table(obj.bol_number)],

            [Paragraph(_('Pickup #'), styles['Normal']),
                string_table(obj.pickup_number)],

            [Paragraph(_('CC #'), styles['Normal']),
                string_table(obj.cc_number)],

            [Paragraph(_('AWB #'), styles['Normal']),
                string_table(obj.awb_number)],

            [Paragraph(_('BL #'), styles['Normal']),
                string_table(obj.bl_number)],

            [Paragraph(_('HBL #'), styles['Normal']),
                string_table(obj.hbl_number)],

            [Paragraph(_('CNTR #'), styles['Normal']),
                string_table(obj.cntr_number)],

            [Paragraph(_('Entry #'), styles['Normal']),
                string_table(obj.entry_number)],

            [Paragraph(_('Carrier'), styles['Normal']),
                string_table(obj.carrier)],

        ]
        shipment_information_a_table = Table(
            shipment_information_a,
            colWidths=(2.3*cm, 7.2*cm),
            hAlign='LEFT',
        )
        shipment_information_a_table.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))
        shipment_information_b = [
            [Paragraph(_('Inbond'), styles['Normal']),
                bool_table(obj.inbond),
                Paragraph(_('Est. Time of Delivery'), styles['Normal']),
                date_table(obj.etd)],

            [Paragraph(_('Hazardous Cargo'), styles['Normal']),
                bool_table(obj.hazardous_cargo),
                Paragraph(_('Est. Time of Arrival #1'), styles['Normal']),
                date_table(obj.eta_1)],

            [Paragraph(_('Skids Exchange'), styles['Normal']),
                bool_table(obj.skids_exchange),
                Paragraph(_('Est. Time of Arrival #2'), styles['Normal']),
                date_table(obj.eta_2)],

            [Paragraph(_('OBL To Shipping Line Sent'), styles['Normal']),
                bool_table(obj.obl_to_shipping_line_sent),
                Paragraph(_('OBL To Shipping Line Sent DT'), styles['Normal']),
                date_table(obj.obl_to_shipping_line_sent_date)],

            [Paragraph(_('Documents To Broker Sent'), styles['Normal']),
                bool_table(obj.documents_to_broker_sent),
                Paragraph(_('Documents To Broker Sent DT'), styles['Normal']),
                date_table(obj.documents_to_broker_sent_date)],

            [Paragraph(_('Documents To Carrier Sent'), styles['Normal']),
                bool_table(obj.documents_to_carrier_sent),
                Paragraph(_('Documents To Carrier Sent DT'), styles['Normal']),
                date_table(obj.documents_to_carrier_sent_date)],

            [Paragraph(_('Arrival Notice Received'), styles['Normal']),
                bool_table(obj.arrival_notice_received),
                Paragraph(_('Arrival Notice Received DT'), styles['Normal']),
                date_table(obj.arrival_notice_received_date)],

            [Paragraph(_('ISF Filled'), styles['Normal']),
                bool_table(obj.isf_filled),
                Paragraph(_('ISF Filled DT'), styles['Normal']),
                date_table(obj.isf_filled_date)],

            [Paragraph(_('Storage Start DT'), styles['Normal']),
                date_table(obj.storage_start_date),
                Paragraph(_('Release DT'), styles['Normal']),
                date_table(obj.release_date)],

        ]
        shipment_information_b_table = Table(
            shipment_information_b,
            colWidths=(
                5*cm,
                2.4*cm,
                5.5*cm,
                2.4*cm
            ),
            hAlign='LEFT',
        )
        shipment_information_b_table.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (4, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))
        shipment_information_c = [
            [shipment_information_a_table, shipment_information_b_table]
        ]
        shipment_information_c_table = Table(
            shipment_information_c,
            hAlign='LEFT',
        )
        shipment_information_c_table.setStyle(TableStyle(
            [
                ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
                ('BOX', (0, 0), (-1, -1), 0, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]
        ))

        # Cargo Description.
        print_cargo_table = False
        cargo_header = Paragraph(
            _('Cargos'), styles['Heading2']
        )
        if Cargo.objects.filter(docket=obj.id).count() != 0:
            print_cargo_table = True
            cargo = []
            cargo.append(
                [
                    Paragraph(_('Description'), styles['Normal']),
                    Paragraph(_('Quantity'), styles['Normal']),
                    Paragraph(_('Piece Unit'), styles['Normal']),
                    Paragraph(_('Weight'), styles['Normal']),
                    Paragraph(_('Unit'), styles['Normal']),
                    Paragraph(_('Length'), styles['Normal']),
                    Paragraph(_('Width'), styles['Normal']),
                    Paragraph(_('Height'), styles['Normal']),
                    Paragraph(_('Unit'), styles['Normal'])
                ]
            )
            for i in Cargo.objects.filter(docket=obj.id):
                cargo.append(
                    [
                        string_table(i.description),
                        string_table(i.quantity),
                        string_table(i.piece_unit),
                        string_table(i.weight),
                        string_table(i.weight_unit),
                        string_table(i.length),
                        string_table(i.width),
                        string_table(i.height),
                        string_table(i.dimension_unit)
                    ]
                )
                cargo_table = Table(
                    cargo,
                    colWidths=(
                        11*cm, 2*cm, 2.2*cm, 2*cm,
                        1.2*cm, 2*cm, 2*cm, 2*cm, 1.2*cm
                    ),
                    hAlign='LEFT',
                )
                cargo_table.setStyle(TableStyle(
                    [
                        ('GRID', (0, 0), (9, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]
                ))

        # Supplier Billing.
        print_supplier_table = False
        supplier_billing_header = Paragraph(
            _('Supplier Billings'), styles['Heading2']
        )
        if SupplierBilling.objects.filter(docket=obj.id).count() != 0:
            print_supplier_table = True
            supplier_billing = []
            supplier_billing.append(
                [
                    Paragraph(_('BT No. #'), styles['Normal']),
                    Paragraph(_('Supplier'), styles['Normal']),
                    Paragraph(_('Supplier Service'), styles['Normal']),
                    Paragraph(_('CCY'), styles['Normal']),
                    Paragraph(_('PX'), styles['Normal']),
                    Paragraph(_('XR'), styles['Normal']),
                    Paragraph(_('Bill No. #'), styles['Normal']),
                    Paragraph(_('RCV'), styles['Normal']),
                    Paragraph(_('APV'), styles['Normal']),
                    Paragraph(_('REC'), styles['Normal']),
                    Paragraph(_('Paid'), styles['Normal']),
                    Paragraph(_('Dis.'), styles['Normal']),
                    Paragraph(_('PY. Date'), styles['Normal']),
                    Paragraph(_('PY. Type'), styles['Normal']),
                    Paragraph(_('PY. TN.'), styles['Normal'])
                ]
            )

            for i in SupplierBilling.objects.filter(docket=obj.id):
                supplier_billing.append(
                    [
                        string_table(i.bill_to),
                        string_table(i.supplier),
                        string_table(i.supplier_service),
                        string_table(i.currency),
                        string_table(i.price),
                        string_table(i.exchange_rate),
                        string_table(i.bill_no),
                        bool_table(i.bill_received),
                        bool_table(i.bill_approved),
                        bool_table(i.bill_recorded),
                        bool_table(i.bill_paid),
                        bool_table(i.bill_dispute),
                        date_table(i.payment_date),
                        string_table(i.payment_type),
                        string_table(i.payment_transfer_number)
                    ]
                )
            supplier_billing_table = Table(
                supplier_billing,
                colWidths=(
                    1*cm, 2.4*cm, 2.6*cm, 1.6*cm, 1.6*cm,
                    1.6*cm, 2*cm, 1.2*cm, 1.2*cm, 1.2*cm,
                    1.2*cm, 1.2*cm, 2.4*cm, 2.4*cm, 2*cm
                ),
                hAlign='LEFT',
            )
            supplier_billing_table.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (15, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]
            ))

        # Customer Billing.
        print_customer_table = False
        customer_billing_header = Paragraph(
            _('Customer Billings'), styles['Heading2']
        )
        if CustomerBilling.objects.filter(docket=obj.id).count() != 0:
            print_customer_table = True
            customer_billing = []
            customer_billing.append(
                [
                    Paragraph(_('BT No. #'), styles['Normal']),
                    Paragraph(_('Customer Company'), styles['Normal']),
                    Paragraph(
                        _('Customer Individual'), styles['Normal']
                    ),
                    Paragraph(_('Customer Service'), styles['Normal']),
                    Paragraph(_('CCY'), styles['Normal']),
                    Paragraph(_('PX'), styles['Normal']),
                    Paragraph(_('XR'), styles['Normal']),
                    Paragraph(_('Invoice No. #'), styles['Normal'])
                ]
            )

            for i in CustomerBilling.objects.filter(docket=obj.id):
                if i.customer_individual is not None:
                    individual = Individual.objects.get(
                        id=str(i.customer_individual)
                    ).get_full_name()
                else:
                    individual = i.customer_individual
                    customer_billing.append(
                        [
                            string_table(i.bill_to),
                            string_table(i.customer_company),
                            string_table(individual),
                            string_table(i.customer_service),
                            string_table(i.currency),
                            string_table(i.price),
                            string_table(i.exchange_rate),
                            string_table(i.invoice_no)
                        ]
                    )
                customer_billing_table = Table(
                    customer_billing,
                    colWidths=(
                        1.9*cm, 4*cm, 4*cm, 4.4*cm,
                        1.2*cm, 2.5*cm, 2*cm, 5.6*cm
                    ),
                    hAlign='LEFT',
                )
                customer_billing_table.setStyle(TableStyle(
                    [
                        ('GRID', (0, 0), (15, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]
                ))

        # Payment Details.
        print_payment_table = False
        payment_header = Paragraph(
            _('Payments'), styles['Heading2']
        )
        if Payment.objects.filter(docket=obj.id).count() != 0:
            print_payment_table = True
            payment = []
            payment.append(
                [
                    Paragraph(_('Invoice #'), styles['Normal']),
                    Paragraph(_('INV BAK Sent'), styles['Normal']),
                    Paragraph(
                        _('INV BAK Sent Date'), styles['Normal']
                    ),
                    Paragraph(_('P Type'), styles['Normal']),
                    Paragraph(
                        _('P Transfer Number'), styles['Normal']
                    )
                ]
            )

            for i in Payment.objects.filter(docket=obj.id):
                payment.append(
                    [
                        string_table(i.invoice_no),
                        string_table(i.invoice_backup_sent),
                        date_table(i.invoice_backup_sent_date),
                        string_table(i.payment_type),
                        string_table(i.payment_transfer_number),
                    ]
                )
            payment_table = Table(
                payment,
                colWidths=(5.9*cm, 4.6*cm, 4.6*cm, 4.6*cm, 5.9*cm),
                hAlign='LEFT',
            )
            payment_table.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (15, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]
            ))

        # Comments
        comment_table = False
        comments_header = Paragraph(
            'Coments and Notes', styles['Heading1']
        )
        if obj.dispute_notes != '' and obj.comment != '' and \
                obj.shipment_notes != '' and obj.customer_notes != '':
            comment_table = True
            dispute_notes = Paragraph(
                str(obj.dispute_notes), styles["Normal"]
            )
            comments = Paragraph(
                str(obj.comment), styles["Normal"]
            )
            shipment_notes = Paragraph(
                str(obj.shipment_notes), styles["Normal"]
            )
            customer_notes = Paragraph(
                str(obj.customer_notes), styles["Normal"]
            )
            comments = [
                [
                    Paragraph('Dispute Notes', styles['Normal']),
                    dispute_notes,
                    Paragraph('Shipment Notes', styles['Normal']),
                    shipment_notes
                ],
                [
                    Paragraph('Comments', styles['Normal']),
                    comments,
                    Paragraph('Customer Notes', styles['Normal']),
                    customer_notes
                ],
            ]
            comments_table = Table(
                comments,
                colWidths=(3*cm, 9.5*cm, 3*cm, 9.5*cm),
                hAlign='LEFT'
            )
            comments_table.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (4, -1), 0, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]
            ))

        # Document structure

        content.append(header_table)
        content.append(Spacer(width=0, height=0.5*cm))
        content.append(top_row_table)
        content.append(Spacer(width=0, height=0.5*cm))
        content.append(shipment_information_header)
        content.append(Spacer(width=0, height=0.5*cm))
        content.append(shipment_information_c_table)
        content.append(Spacer(width=0, height=3*cm))

        if print_cargo_table is True:
            content.append(cargo_header)
            content.append(Spacer(width=0, height=0.5*cm))
            content.append(cargo_table)
            content.append(Spacer(width=0, height=0.5*cm))

        if print_supplier_table is True:
            content.append(supplier_billing_header)
            content.append(Spacer(width=0, height=0.5*cm))
            content.append(supplier_billing_table)
            content.append(Spacer(width=0, height=0.5*cm))

        if print_customer_table is True:
            content.append(customer_billing_header)
            content.append(Spacer(width=0, height=0.5*cm))
            content.append(customer_billing_table)
            content.append(Spacer(width=0, height=0.5*cm))

        if print_payment_table is True:
            content.append(payment_header)
            content.append(Spacer(width=0, height=0.5*cm))
            content.append(payment_table)
            content.append(Spacer(width=0, height=0.5*cm))

        if comment_table is True:
            content.append(comments_header)
            content.append(Spacer(width=0, height=0.5*cm))
            content.append(comments_table)

        doc.build(content)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' \
            + str(_('Docket')) + ' ' + str(_('Report')) + ' - ' \
            + str(obj.docket_number_id) + '.pdf"'
        response.write(buff.getvalue())
        return response
