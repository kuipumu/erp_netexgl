"""netexgl.models.py"""

from uuid import uuid4

from django.contrib.postgres.fields import CITextField
from django.db.models import (CASCADE, DateTimeField, ForeignKey, Model,
                              UUIDField)
from django.utils.translation import ugettext_lazy as _


class BaseModel(Model):
    """Define base abstract model."""
    id = UUIDField(
        'ID',
        primary_key=True,
        default=uuid4,
        editable=False
    )
    note = CITextField(
        _('Note'),
        blank=True,
        null=True
    )
    created_at = DateTimeField(
        _('Created At'),
        auto_now_add=True,
        editable=False
    )
    updated_at = DateTimeField(
        _('Updated At'),
        auto_now=True,
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        """Model meta."""
        abstract = True
        ordering = ['-created_at']
