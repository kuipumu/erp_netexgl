"""thirdparty.models.py"""

from django.contrib.postgres.fields import CICharField, CIEmailField
from django.db.models import (BigIntegerField, DateField, ManyToManyField,
                              PositiveIntegerField, URLField)
from django.utils.translation import ugettext_lazy as _
from netexgl.data import COUNTRIES
from netexgl.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class Individual(BaseModel):
    """Define individual model."""
    first_name = CICharField(
        _('First Name'),
        max_length=100,
        blank=False,
        null=False
    )
    last_name = CICharField(
        _('Last Name'),
        max_length=100,
        blank=True,
        null=True
    )
    address_line1 = CICharField(
        _('Address Line 1'),
        max_length=255,
        blank=True,
        null=True
    )
    address_line2 = CICharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        null=True
    )
    city_district = CICharField(
        _('City / District'),
        max_length=255,
        blank=True,
        null=True
    )
    state_province = CICharField(
        _('State / Province'),
        max_length=255,
        blank=True,
        null=True
    )
    postal_code = CICharField(
        _('ZIP C. / Postal C.'),
        max_length=50,
        blank=True,
        null=True
    )
    country = CICharField(
        _('Country'),
        max_length=150,
        choices=COUNTRIES,
        blank=True,
        null=True
    )
    phone_number_1 = PhoneNumberField(
        _('Phone Number #1'),
        blank=True,
        null=True,
    )
    extension_1 = PositiveIntegerField(
        _('Extension #1'),
        blank=True,
        null=True
    )
    phone_number_2 = PhoneNumberField(
        _('Phone Number #2'),
        blank=True,
        null=True,
    )
    extension_2 = PositiveIntegerField(
        _('Extension #2'),
        blank=True,
        null=True
    )
    mobile_number = PhoneNumberField(
        _('Mobile Number'),
        blank=True,
        null=True,
    )
    fax_number = PhoneNumberField(
        _('Fax Number'),
        blank=True,
        null=True,
    )
    email = CIEmailField(
        _('Email Address'),
        blank=True,
        null=True,
        unique=True
    )
    website = URLField(
        _('Website'),
        blank=True,
        null=True,
        unique=True
    )

    def get_full_name(self):
        """Get the full name of individual."""
        if self.last_name is not None:
            full_name = "{0} {1}".format(self.first_name, self.last_name)
            full_name.strip()
        else:
            full_name = self.first_name
        return full_name

    def __str__(self):
        return str(self.get_full_name())


class Company(BaseModel):
    """Define the model in the database."""
    company_name = CICharField(
        _('Company Name'),
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    address_line1 = CICharField(
        _('Address Line 1'),
        max_length=255,
        blank=True,
        null=True
    )
    address_line2 = CICharField(
        _('Address Line 2'),
        max_length=255,
        blank=True,
        null=True
    )
    city_district = CICharField(
        _('City / District'),
        max_length=255,
        blank=True,
        null=True
    )
    state_province = CICharField(
        _('State / Province'),
        max_length=255,
        blank=True,
        null=True
    )
    postal_code = CICharField(
        _('ZIP C. / Postal C.'),
        max_length=50,
        blank=True,
        null=True
    )
    country = CICharField(
        _('Country'),
        max_length=150,
        choices=COUNTRIES,
        blank=True,
        null=True
    )
    importer_number = BigIntegerField(
        _('Importer #'),
        blank=True,
        null=True,
        unique=True
    )
    setup_date = DateField(
        _('Setup Date'),
        blank=True,
        null=True
    )
    phone_number_1 = PhoneNumberField(
        _('Phone Number #1'),
        blank=True,
        null=True,
    )
    extension_1 = PositiveIntegerField(
        _('Extension #1'),
        blank=True,
        null=True
    )
    phone_number_2 = PhoneNumberField(
        _('Phone Number #2'),
        blank=True,
        null=True,
    )
    extension_2 = PositiveIntegerField(
        _('Extension #2'),
        blank=True,
        null=True
    )
    mobile_number = PhoneNumberField(
        _('Mobile Number'),
        blank=True,
        null=True,
    )
    fax_number = PhoneNumberField(
        _('Fax Number'),
        blank=True,
        null=True,
    )
    email = CIEmailField(
        _('Email'),
        blank=True,
        null=True,
    )
    website = URLField(
        _('Website'),
        blank=True,
        null=True,
        unique=True
    )
    individuals = ManyToManyField(
        Individual,
        verbose_name=_('Individual'),
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('companies')

    def __str__(self):
        return str(self.company_name)
