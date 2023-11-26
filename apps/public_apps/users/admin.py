from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin, ImportExportActionModelAdmin):
    search_fields = (
        'id',
        'username',
        'email',
        'cell_phone',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_business_admin',
    )

    list_display = (
        'id',
        'get_full_name',
        'username',
        'email',
        'cell_phone',
        'is_business_admin',
        'is_staff',
        'is_active'
    )

    list_display_links = (
        'id',
        'get_full_name',
        'username',
        'email',
    )

    ordering = (
        'default_order',
        'id',
        'is_business_admin',
        'first_name',
        'last_name',
        'email',
        'username',
    )

    readonly_fields = (
        'created',
        'updated',
        'last_login',
        'get_age'
    )

    fieldsets = (
        (
            _('Información de usuario'), {
                'fields': (
                    'username',
                    'password'
                )
            }
        ),
        (
            _('Información personal'), {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'cell_phone',
                    'birthday',
                    'get_age',
                )
            }
        ),
        (
            _('Permisos'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_business_admin',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (
            _('Fechas'), {
                'fields': (
                    'last_login',
                    'created',
                    'updated'
                )
            }
        ),
        (
            _('Orden por defecto'), {
                'fields': (
                    'default_order',
                )
            }
        )
    )

    def get_age(self, obj):
        return obj.get_age()

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = _('Full name')

    get_age.short_description = _('Age')
