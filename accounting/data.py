"""accounting data.py"""

from django.utils.translation import ugettext_lazy as _

BILL_TO_N = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
]

CURRENCY_TYPES = [
    (_('USD'), _('USD')),
    (_('CAD'), _('CAD')),
]

PAYMENT_TYPES = [
    (_('Cash'), _('Cash')),
    (_('Check'), _('Check')),
    (_('Credit Card'), _('Credit Card')),
    (_('EFT'), _('EFT')),
    (_('Wire Transfer'), _('Wire Transfer')),
    (_('Direct Deposit'), _('Direct Deposit')),
]

SUPPLIER_AND_CUSTOMER_SERVICES = [
    (_('Customs Duty'), _('Customs Duty')),
    (_('Customs GST'), _('Customs GST')),
    (_('Brokerage'), _('Brokerage')),
    (_('Freight'), _('Freight')),
    (_('Terminal / Handling'), _('Terminal / Handling')),
    (_('Documentation'), _('Documentation')),
    (_('Cartage #1'), _('Cartage #1')),
    (_('Cartage #2'), _('Cartage #2')),
    (_('Liftgate Fee'), _('Liftgate Fee')),
    (_('Appointment Fee'), _('Appointment Fee')),
    (_('Export Docs'), _('Export Docs')),
    (_('Airline Transfer'), _('Airline Transfer')),
    (_('Waiting Time'), _('Waiting Time')),
    (_('Bond Charges'), _('Bond Charges')),
    (_('Import Permits'), _('Import Permits')),
    (_('Packaging Charges'), _('Packaging Charges')),
    (_('Courier'), _('Courier')),
    (_('Storage Charges'), _('Storage Charges')),
    (_('Warehouse In'), _('Warehouse In')),
    (_('Warehouse Out'), _('Warehouse Out')),
    (_('Fuel Surcharge'), _('Fuel Surcharge')),
    (_('Nav. Canada Fees'), _('Nav. Canada Fees')),
    (_('Security Surcharge'), _('Security Surcharge')),
    (_('Border Security Charge'), _('Border Security Charge')),
    (_('Doc Charges'), _('Doc Charges')),
    (_('Customs Exams Charge'), _('Customs Exams Charge')),
    (_('DUI Agent Fee'), _('DUI Agent Fee')),
    (_('Insurance Fee'), _('Insurance Fee')),
    (_('Paying Charge'), _('Paying Charge')),
    (_('Outport Fee'), _('Outport Fee')),
    (_('ISF'), _('ISF')),
    (_('MPF'), _('MPF')),
    (_('Line Fee'), _('Line Fee')),
    (_('Funds Advance'), _('Funds Advance')),
    (_('FCC'), _('FCC')),
    (_('Labour Fee'), _('Labour Fee')),
    (_('Consolidation Fee'), _('Consolidation Fee')),
    (_('Administrative Charges'), _('Administrative Charges')),
    (_('Attempted Pickup'), _('Attempted Pickup')),
    (_('Terminal Fee'), _('Terminal Fee')),
    (_('Terminal Handling'), _('Terminal Handling')),
    (_('Export Declaration'), _('Export Declaration')),
    (_('Destuffing'), _('Destuffing')),
    (_('Miscellaneous'), _('Miscellaneous')),
]
