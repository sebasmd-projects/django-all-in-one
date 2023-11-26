import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_core.settings')

app = TenantAwareCeleryApp('app_core')

app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(timezone='America/Bogota')
app.conf.update(
    result_backend='django-db',
)

app.conf.task_serializer = 'json'
app.conf.broker_connection_retry_on_startup = True


@app.task(bind=True)
def debug_task(self):
    from apps.public_apps.errors.models import ExceptionModel
    print('Request: {0!r}'.format(self.request))

    error_message = f"Request: {self.request}"
    error_type = "Celery error"
    source = "Celery task"

    ExceptionModel.objects.create(
        message=error_message,
        error_type=error_type,
        source=source
    )
