from datetime import date

from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, CharField, DateField
from django.utils.translation import gettext_lazy as _

from apps.public_apps.utils.models import TimeStampedModel


class UserModel(TimeStampedModel, AbstractUser):
    is_business_admin = BooleanField(
        _('administrador de negocio'),
        default=False
    )

    cell_phone = CharField(
        _('teléfono'),
        max_length=15,
        null=True,
        blank=True
    )

    birthday = DateField(
        _('fecha de nacimiento'),
        default=date.today,
        blank=True,
        null=True
    )

    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name'
    ]

    def get_age(self):
        return date.today().year - self.birthday.year - (
            (date.today().month, date.today().day) < (
                self.birthday.month, self.birthday.day)
        )

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        self.username = self.username.lower()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.get_full_name()

    class Meta:
        db_table = 'apps_public_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')


auditlog.register(
    UserModel,
    serialize_data=True
)
