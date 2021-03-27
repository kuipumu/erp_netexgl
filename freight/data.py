"""freight data.py"""

from django.utils.translation import ugettext_lazy as _

DIMENSION_UNITS = [
    (_('Inch'), _('Inch')),
    (_('Feet'), _('Feet')),
    (_('Cm'), _('Cm')),
    (_('Cbm'), _('Cbm')),
    (_('Cbf'), _('Cbf')),
]

WEIGHT_UNITS = [
    ('Lb', 'Lb'),
    ('Kg', 'Kg'),
    ('Ton', 'Ton'),
]

UNIT_TYPES = [
    (_('Box'), _('Box')),
    (_('Container'), _('Container')),
    (_('Skid'), _('Skid')),
    (_('Crate'), _('Crate')),
    (_('Flatbed'), _('Flatbed')),
    (_('Ftl'), _('Ftl')),
    (_('Bundle'), _('Bundle')),
    (_('Packages'), _('Packages')),
    (_('Roll'), _('Roll')),
    (_('Engine'), _('Engine')),
    (_('Rolling Printers'), _('Rolling Printers')),
    (_('Pipe'), _('Pipe')),
    (_('Envelope'), _('Envelope')),
    (_('Hoist'), _('Hoist')),
    (_('Express Letter'), _('Express Letter')),
    (_('Documents'), _('Documents')),
    (_('Miscellaneous'), _('Miscellaneous')),
]

DOCKET_TYPES = [
    ('Import', 'Import'),
    ('Export', 'Export'),
]
