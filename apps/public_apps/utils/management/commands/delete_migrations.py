import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete all migration files and folders except __init__.py, and custom apps'
    base_dir = settings.BASE_DIR

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '-sp',
            '--skippermanent',
            dest='skippermanent',
            type=str,
            help='Skip permanent app migrations'
        )
        parser.add_argument(
            '-s',
            '--skip',
            type=str,
            help='Skip app migrations'
        )

    def handle(self, *args, **options):
        skip_permanent = options.get('skippermanent', None)
        skip_current = options.get('skip', None)

        deleted_folders = []
        deleted_files = []
        exceptions = []

        skip_apps = self.get_write_file(skip_permanent)

        if skip_current and skip_current not in skip_apps:
            skip_apps.append(skip_current)

        for app_path in settings.CUSTOM_APPS:
            app_name = app_path.split('.')[-1]

            if app_name in skip_apps:
                continue

            migration_dir = os.path.join(
                self.base_dir, app_path.replace('.', os.path.sep), 'migrations'
            )

            try:
                pycache_dir = os.path.join(migration_dir, '__pycache__')
                if os.path.exists(pycache_dir):
                    for item in os.listdir(pycache_dir):
                        pycache_item = os.path.join(pycache_dir, item)
                        if os.path.isfile(pycache_item):
                            os.remove(pycache_item)
                        elif os.path.isdir(pycache_item):
                            os.rmdir(pycache_item)
                    os.rmdir(pycache_dir)
                    deleted_folders.append((app_name, '__pycache__'))

                for filename in os.listdir(migration_dir):
                    if filename != '__init__.py' and filename.endswith('.py'):
                        migration_file = os.path.join(migration_dir, filename)
                        os.remove(migration_file)
                        deleted_files.append((app_name, filename))
            except FileNotFoundError as e:
                exceptions.append(str(e))

        if deleted_folders:
            self.print_deleted(deleted_folders, 'DELETED', self.style.WARNING)
        else:
            self.stdout.write(
                self.style.ERROR(
                    'No folders found or have already been deleted')
            )

        if deleted_files:
            self.print_deleted(deleted_files, 'DELETED', self.style.SUCCESS)
        else:
            self.stdout.write(
                self.style.ERROR(
                    'No files found or have already been deleted')
            )

        if exceptions:
            self.print_exceptions(exceptions)

    def print_deleted(self, items, action, style):
        for app_name, name in items:
            self.stdout.write(style(f'\n{app_name}\n{name} {action}'))

    def print_exceptions(self, exceptions):
        self.stdout.write(self.style.ERROR("\nExcepciones FileNotFound:"))
        for exception in exceptions:
            self.stdout.write(self.style.ERROR(f"- {exception}"))

    def print_skiped(self, items):
        self.stdout.write(self.style.SUCCESS(
            f'Skipped apps: {items}')
        )

    def get_write_file(self, app_name: str = None) -> list:
        apps_names_file_path = os.path.join(
            self.base_dir, "apps", "public_apps", "utils", "data", "skip_apps.txt"
        )

        with open(apps_names_file_path, 'r') as apps_names_file:
            skip_apps = apps_names_file.read().split(',')

        if app_name and app_name not in skip_apps:
            skip_apps.append(app_name)

            with open(apps_names_file_path, 'w') as apps_names_file:
                apps_names_file.write(','.join(skip_apps))

        self.print_skiped(skip_apps)

        return skip_apps
