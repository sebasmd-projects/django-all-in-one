from auditlog.models import AuditlogHistoryField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    history = AuditlogHistoryField()

    created = models.DateTimeField(
        _('created'),
        default=timezone.now
    )

    updated = models.DateTimeField(
        _('updated'),
        auto_now=True
    )

    default_order = models.PositiveIntegerField(
        _('default order'),
        default=1,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
